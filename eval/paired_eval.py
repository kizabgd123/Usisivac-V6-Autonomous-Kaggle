#!/usr/bin/env python3
"""Fail-closed paired five-seed OOF AUC promotion gate."""
from __future__ import annotations

import argparse
import json
import math
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

import numpy as np
import scipy
from scipy.stats import t as student_t

CANONICAL_SEEDS = (42, 43, 44, 45, 46)
ALPHA = 0.05


class EvaluationError(ValueError):
    """Invalid or incomplete evaluation input."""


class PromotionBlocked(RuntimeError):
    """Raised when promotion is attempted without a valid PROMOTE verdict."""


def runtime_environment() -> dict[str, str]:
    import sklearn
    return {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "scikit_learn": sklearn.__version__,
    }


def _scores_by_seed(values: Mapping[Any, Any] | Sequence[Any], label: str) -> dict[int, float]:
    if isinstance(values, Mapping):
        normalized: dict[int, float] = {}
        for key, value in values.items():
            try:
                seed = int(key)
            except (TypeError, ValueError) as exc:
                raise EvaluationError(f"{label} has a non-integer seed key: {key!r}") from exc
            if seed in normalized:
                raise EvaluationError(f"{label} contains duplicate seed {seed}")
            normalized[seed] = float(value)
    else:
        if isinstance(values, (str, bytes)) or len(values) != len(CANONICAL_SEEDS):
            raise EvaluationError(f"{label} must contain exactly five seed scores")
        normalized = {seed: float(value) for seed, value in zip(CANONICAL_SEEDS, values)}

    if set(normalized) != set(CANONICAL_SEEDS):
        raise EvaluationError(f"{label} must use canonical seeds {list(CANONICAL_SEEDS)}")
    for seed, score in normalized.items():
        if not math.isfinite(score) or not 0.0 <= score <= 1.0:
            raise EvaluationError(f"{label}[{seed}] must be a finite AUC in [0, 1]")
    return normalized


def evaluate_paired_scores(
    baseline_auc: Mapping[Any, Any] | Sequence[Any],
    candidate_auc: Mapping[Any, Any] | Sequence[Any],
    *,
    seeds: Sequence[int] = CANONICAL_SEEDS,
    alpha: float = ALPHA,
    environment: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    """Compute a two-sided paired t-test and two-sided 95% confidence interval."""
    seed_list = [int(s) for s in seeds]
    if seed_list != list(CANONICAL_SEEDS):
        raise EvaluationError(f"Promotion requires canonical seeds {list(CANONICAL_SEEDS)}")
    if not math.isfinite(float(alpha)) or float(alpha) != ALPHA:
        raise EvaluationError("Issue #7 fixes the significance threshold at alpha=0.05")

    base = _scores_by_seed(baseline_auc, "baseline_auc")
    cand = _scores_by_seed(candidate_auc, "candidate_auc")
    deltas = np.asarray([cand[s] - base[s] for s in seed_list], dtype=float)
    n = len(deltas)
    df = n - 1
    mean_delta = float(np.mean(deltas))
    corrected_std = float(np.std(deltas, ddof=1))
    standard_error = corrected_std / math.sqrt(n)

    if corrected_std == 0.0 or not math.isfinite(standard_error):
        # Degenerate paired samples are undefined for a t-test; never promote them.
        t_statistic, p_value = 0.0, 1.0
        ci_lower = ci_upper = mean_delta
    else:
        t_statistic = float(mean_delta / standard_error)
        p_value = float(2.0 * student_t.sf(abs(t_statistic), df=df))
        critical = float(student_t.ppf(1.0 - ALPHA / 2.0, df=df))
        margin = critical * standard_error
        ci_lower, ci_upper = float(mean_delta - margin), float(mean_delta + margin)

    verdict = "PROMOTE" if p_value < ALPHA and ci_lower > 0.0 else "HOLD"
    matrix = [
        {
            "seed": seed,
            "baseline_auc": base[seed],
            "candidate_auc": cand[seed],
            "delta": float(cand[seed] - base[seed]),
        }
        for seed in seed_list
    ]
    return {
        "schema_version": 1,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "seeds": seed_list,
        "evaluation_matrix": matrix,
        "summary": {
            "n_seeds": n,
            "degrees_of_freedom": df,
            "mean_delta": mean_delta,
            "corrected_std": corrected_std,
            "standard_error": float(standard_error),
            "t_statistic": t_statistic,
            "p_value": p_value,
            "alpha": ALPHA,
            "confidence_level": 0.95,
            "ci_lower": ci_lower,
            "ci_upper": ci_upper,
            "verdict": verdict,
        },
        "runtime_environment": dict(environment or runtime_environment()),
    }


def append_eval_history(report: Mapping[str, Any], path: str | Path = "eval/eval_history.jsonl") -> Path:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(report, sort_keys=True, allow_nan=False) + "\n")
        handle.flush()
    return destination


def require_promote(report: Mapping[str, Any]) -> None:
    """Recompute the verdict from the score matrix to reject forged summary flags."""
    try:
        if list(report["seeds"]) != list(CANONICAL_SEEDS):
            raise PromotionBlocked(f"Promotion requires seeds {list(CANONICAL_SEEDS)}")
        matrix = report["evaluation_matrix"]
        if len(matrix) != len(CANONICAL_SEEDS):
            raise PromotionBlocked("Evaluation report must contain exactly five seed rows")
        baseline = {int(row["seed"]): float(row["baseline_auc"]) for row in matrix}
        candidate = {int(row["seed"]): float(row["candidate_auc"]) for row in matrix}
        summary = report["summary"]
        recomputed = evaluate_paired_scores(baseline, candidate)
    except (KeyError, TypeError, ValueError, EvaluationError) as exc:
        if isinstance(exc, PromotionBlocked):
            raise
        raise PromotionBlocked(f"Invalid evaluation report: {exc}") from exc

    expected = recomputed["summary"]
    if float(summary.get("alpha", -1)) != ALPHA or float(summary.get("confidence_level", -1)) != 0.95:
        raise PromotionBlocked("Report does not use the required alpha=0.05 and confidence_level=0.95")
    for field in ("mean_delta", "corrected_std", "t_statistic", "p_value", "ci_lower", "ci_upper"):
        try:
            actual = float(summary[field])
        except (KeyError, TypeError, ValueError) as exc:
            raise PromotionBlocked(f"Report is missing summary field {field}") from exc
        if not math.isclose(actual, float(expected[field]), rel_tol=1e-10, abs_tol=1e-12):
            raise PromotionBlocked(f"Summary field {field} does not match the score matrix")
    if summary.get("verdict") != expected["verdict"] or expected["verdict"] != "PROMOTE":
        raise PromotionBlocked(
            f"Champion promotion blocked: verdict={expected['verdict']}, "
            f"p={expected['p_value']:.6g}, CI_lower={expected['ci_lower']:.6g}"
        )


def guarded_promote(report: Mapping[str, Any], callback: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
    require_promote(report)
    return callback(*args, **kwargs)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="JSON with baseline_auc and candidate_auc keyed by seed")
    parser.add_argument("--history", type=Path, default=Path("eval/eval_history.jsonl"))
    parser.add_argument("--report", type=Path, default=Path("eval/latest_eval.json"))
    args = parser.parse_args(argv)
    try:
        payload = json.loads(args.input.read_text(encoding="utf-8"))
        report = evaluate_paired_scores(payload["baseline_auc"], payload["candidate_auc"])
        append_eval_history(report, args.history)
        args.report.parent.mkdir(parents=True, exist_ok=True)
        tmp = args.report.with_suffix(args.report.suffix + ".tmp")
        tmp.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
        tmp.replace(args.report)
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        parser.error(str(exc))
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["summary"]["verdict"] == "PROMOTE" else 1


if __name__ == "__main__":
    raise SystemExit(main())
