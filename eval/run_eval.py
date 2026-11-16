#!/usr/bin/env python3
"""Run five-seed paired OOF ROC-AUC evaluation using a project model adapter.

Adapter contract: fit_predict_fold(X_train, y_train, X_valid, *, seed, fold)
returns {"baseline": probability_vector, "candidate": probability_vector}.
Both models must be fitted in that one call on the same training partition.
"""
from __future__ import annotations

import argparse
import importlib
import json
import os
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold

try:
    from .paired_eval import CANONICAL_SEEDS, EvaluationError, append_eval_history, evaluate_paired_scores
except ImportError:
    from paired_eval import CANONICAL_SEEDS, EvaluationError, append_eval_history, evaluate_paired_scores


DEFAULT_PLAN = Path(__file__).with_name("experiment_plan.json")


def load_plan(path: Path = DEFAULT_PLAN) -> dict[str, Any]:
    try:
        plan = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise EvaluationError(f"Cannot load experiment plan {path}: {exc}") from exc
    settings = plan.get("evaluation", {})
    if settings.get("seeds") != list(CANONICAL_SEEDS) or settings.get("metric") != "roc_auc":
        raise EvaluationError("Plan must register the five canonical seeds and roc_auc")
    if int(settings.get("n_splits", 0)) < 2:
        raise EvaluationError("Plan n_splits must be at least 2")
    return plan


def load_adapter(spec: str) -> Callable[..., Mapping[str, Any]]:
    if ":" not in spec:
        raise EvaluationError("Evaluator must use module:function notation")
    module_name, function_name = spec.split(":", 1)
    try:
        adapter = getattr(importlib.import_module(module_name), function_name)
    except (ImportError, AttributeError) as exc:
        raise EvaluationError(f"Cannot import evaluator {spec}: {exc}") from exc
    if not callable(adapter):
        raise EvaluationError(f"Evaluator {spec} is not callable")
    return adapter


def _probabilities(values: Any, size: int, label: str) -> np.ndarray:
    result = np.asarray(values, dtype=float)
    if result.ndim != 1 or len(result) != size:
        raise EvaluationError(f"{label} must be a 1-D probability vector of length {size}")
    if not np.isfinite(result).all() or (result < 0).any() or (result > 1).any():
        raise EvaluationError(f"{label} contains invalid probabilities")
    return result


def run_multiseed_evaluation(
    frame: pd.DataFrame,
    target: str,
    evaluator: Callable[..., Mapping[str, Any]],
    *,
    plan: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    if target not in frame or frame.empty:
        raise EvaluationError(f"Target column {target!r} is missing or dataset is empty")
    y = frame[target].reset_index(drop=True)
    if y.isna().any() or y.nunique() != 2:
        raise EvaluationError("ROC AUC requires a non-missing binary target")
    settings = dict((plan or load_plan()).get("evaluation", {}))
    seeds = settings.get("seeds")
    if seeds != list(CANONICAL_SEEDS):
        raise EvaluationError(f"Only canonical seeds {list(CANONICAL_SEEDS)} are allowed")
    n_splits = int(settings["n_splits"])
    if float(settings.get("alpha", 0.0)) != 0.05 or float(settings.get("confidence_level", 0.0)) != 0.95:
        raise EvaluationError("Plan must use alpha=0.05 and confidence_level=0.95")
    counts = y.value_counts()
    if int(counts.min()) < n_splits:
        raise EvaluationError(f"Each target class must have at least {n_splits} rows")

    X = frame.drop(columns=[target]).reset_index(drop=True)
    baseline_scores: dict[int, float] = {}
    candidate_scores: dict[int, float] = {}
    for seed in seeds:
        baseline_oof = np.full(len(frame), np.nan, dtype=float)
        candidate_oof = np.full(len(frame), np.nan, dtype=float)
        coverage = np.zeros(len(frame), dtype=np.int8)
        splitter = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=int(seed))
        for fold, (train_idx, valid_idx) in enumerate(splitter.split(X, y)):
            result = evaluator(
                X.iloc[train_idx].copy(), y.iloc[train_idx].copy(),
                X.iloc[valid_idx].copy(), seed=int(seed), fold=int(fold)
            )
            if not isinstance(result, Mapping) or not {"baseline", "candidate"} <= set(result):
                raise EvaluationError("Evaluator must return baseline and candidate probabilities")
            baseline_oof[valid_idx] = _probabilities(result["baseline"], len(valid_idx), "baseline")
            candidate_oof[valid_idx] = _probabilities(result["candidate"], len(valid_idx), "candidate")
            coverage[valid_idx] += 1
        if not np.all(coverage == 1) or not np.isfinite(baseline_oof).all() or not np.isfinite(candidate_oof).all():
            raise EvaluationError(f"Seed {seed} did not produce exactly one OOF prediction per row")
        baseline_scores[int(seed)] = float(roc_auc_score(y, baseline_oof))
        candidate_scores[int(seed)] = float(roc_auc_score(y, candidate_oof))
    report = evaluate_paired_scores(baseline_scores, candidate_scores, seeds=seeds)
    report["experiment_id"] = (plan or {}).get("experiment_id")
    report["target_column"] = target
    report["n_rows"] = int(len(frame))
    report["n_splits"] = n_splits
    return report


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", required=True, type=Path, help="Training CSV or Parquet file")
    parser.add_argument("--target", required=True, help="Binary target column")
    parser.add_argument("--evaluator", required=True, help="Adapter in module:function form")
    parser.add_argument("--plan", type=Path, default=DEFAULT_PLAN)
    parser.add_argument("--history", type=Path, default=Path("eval/eval_history.jsonl"))
    parser.add_argument("--report", type=Path, default=Path("eval/latest_eval.json"))
    args = parser.parse_args(argv)
    try:
        plan = load_plan(args.plan)
        os.environ["USISIVAC_EXPERIMENT_PLAN"] = str(args.plan.resolve())
        adapter = load_adapter(args.evaluator)
        if args.data.suffix.lower() == ".csv":
            frame = pd.read_csv(args.data)
        elif args.data.suffix.lower() in {".parquet", ".pq"}:
            frame = pd.read_parquet(args.data)
        else:
            raise EvaluationError("Data file must be CSV or Parquet")
        report = run_multiseed_evaluation(frame, args.target, adapter, plan=plan)
        append_eval_history(report, args.history)
        args.report.parent.mkdir(parents=True, exist_ok=True)
        tmp = args.report.with_suffix(args.report.suffix + ".tmp")
        tmp.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
        tmp.replace(args.report)
    except (EvaluationError, OSError, TypeError, ValueError) as exc:
        parser.error(str(exc))
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["summary"]["verdict"] == "PROMOTE" else 1


if __name__ == "__main__":
    raise SystemExit(main())
