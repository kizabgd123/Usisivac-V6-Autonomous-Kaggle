#!/usr/bin/env python3
"""
paired_eval.py — Multi-Seed Paired Statistical Evaluation Protocol
===================================================================
Computes a paired t-test and 95% confidence interval over per-seed OOF AUC
scores collected from a CSV matrix.

Usage
-----
    python paired_eval.py --matrix eval_matrix.csv \
                          --baseline baseline_auc \
                          --candidate candidate_auc

CSV format expected (one row per seed):
    seed,baseline_auc,candidate_auc
    42,0.892341,0.892713
    43,0.891876,0.892124
    ...

Champion Promotion Criterion (non-negotiable)
---------------------------------------------
A Candidate may be promoted to Champion ONLY IF:
  1.  CI_lower > 0  (lower bound of 95% CI is strictly positive)
  2.  p < 0.05      (two-tailed paired t-test)

Both must hold simultaneously.

Author : kiza / kaggle-eval-protocol plugin v1.0.0
"""

import argparse
import json
import math
import sys
from pathlib import Path

try:
    import numpy as np
    import pandas as pd
    from scipy import stats as scipy_stats
    _SCIPY = True
except ImportError:
    _SCIPY = False


# ---------------------------------------------------------------------------
# Pure-Python fallback (no scipy required) — t-distribution via regularised
# incomplete beta function approximation (Abramowitz & Stegun 26.7.8).
# Accurate to ~1e-5 for df in [1, 50] which covers all use-cases here.
# ---------------------------------------------------------------------------

def _betai(a: float, b: float, x: float) -> float:
    """Regularised incomplete beta I_x(a, b) via continued fraction."""
    if x < 0.0 or x > 1.0:
        raise ValueError("x must be in [0, 1]")
    if x == 0.0:
        return 0.0
    if x == 1.0:
        return 1.0
    lbeta = (
        math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b)
        + a * math.log(x) + b * math.log(1.0 - x)
    )
    # Use CF expansion (Lentz) — symmetry swap for convergence
    if x > (a + 1.0) / (a + b + 2.0):
        return 1.0 - _betai(b, a, 1.0 - x)
    # Modified Lentz
    eps = 1e-10
    fpmin = 1e-30
    qab = a + b
    qap = a + 1.0
    qam = a - 1.0
    c = 1.0
    d = 1.0 - qab * x / qap
    if abs(d) < fpmin:
        d = fpmin
    d = 1.0 / d
    h = d
    for m in range(1, 200):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < fpmin:
            d = fpmin
        c = 1.0 + aa / c
        if abs(c) < fpmin:
            c = fpmin
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < fpmin:
            d = fpmin
        c = 1.0 + aa / c
        if abs(c) < fpmin:
            c = fpmin
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < eps:
            break
    return math.exp(lbeta) * h / a


def _t_sf(t: float, df: int) -> float:
    """Survival function of |t| under t(df): P(T > |t|) one-tail."""
    x = df / (df + t * t)
    return 0.5 * _betai(df / 2.0, 0.5, x)


def _t_ppf(p: float, df: int) -> float:
    """Inverse CDF of t(df) at probability p (two-tail alpha → p=1-alpha/2)."""
    # Binary search — good enough for CI computation
    lo, hi = 0.0, 1000.0
    for _ in range(80):
        mid = (lo + hi) / 2.0
        if _t_sf(mid, df) > 1.0 - p:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


# ---------------------------------------------------------------------------
# Core computation
# ---------------------------------------------------------------------------

def compute_paired_stats(deltas: list) -> dict:
    """
    Given a list of per-seed deltas (candidate - baseline), compute:
      - mean_delta
      - std (corrected, ddof=1)
      - t-statistic
      - p-value (two-tailed)
      - 95% confidence interval (lower, upper)
    """
    n = len(deltas)
    if n < 2:
        raise ValueError(f"Need at least 2 seeds, got {n}")

    mean_d = sum(deltas) / n
    variance = sum((d - mean_d) ** 2 for d in deltas) / (n - 1)
    std_d = math.sqrt(variance)
    se = std_d / math.sqrt(n)
    t_stat = mean_d / se if se > 0 else float("inf")
    df = n - 1

    if _SCIPY:
        p_value = float(scipy_stats.t.sf(abs(t_stat), df=df) * 2)
        t_crit = float(scipy_stats.t.ppf(0.975, df=df))
    else:
        p_value = _t_sf(abs(t_stat), df) * 2
        t_crit = _t_ppf(0.975, df)

    ci_lower = mean_d - t_crit * se
    ci_upper = mean_d + t_crit * se

    return {
        "n_seeds": n,
        "df": df,
        "mean_delta": mean_d,
        "std_delta": std_d,
        "se_delta": se,
        "t_statistic": t_stat,
        "p_value_two_tailed": p_value,
        "ci_95_lower": ci_lower,
        "ci_95_upper": ci_upper,
        "promoted": ci_lower > 0 and p_value < 0.05,
    }


# ---------------------------------------------------------------------------
# Report rendering
# ---------------------------------------------------------------------------

BANNER = "=" * 52

def _fmt(v: float) -> str:
    return f"{v:+.6f}"


def render_report(seeds: list, deltas: list, stats: dict) -> str:
    lines = [
        BANNER,
        "  Multi-Seed Paired Evaluation Report",
        BANNER,
        f"  Seeds evaluated : {seeds}",
        f"  Per-seed deltas : {[_fmt(d) for d in deltas]}",
        f"  Mean delta      : {_fmt(stats['mean_delta'])}",
        f"  Std  (corrected): {stats['std_delta']:+.6f}",
        f"  SE              : {stats['se_delta']:+.6f}",
        f"  t-statistic     : {stats['t_statistic']:.4f}  (df={stats['df']})",
        f"  p-value (2-tail): {stats['p_value_two_tailed']:.6f}",
        f"  95% CI          : [{_fmt(stats['ci_95_lower'])}, {_fmt(stats['ci_95_upper'])}]",
        BANNER,
    ]
    if stats["promoted"]:
        lines.append(
            f"  ✅ PROMOTE: CI_lower = {_fmt(stats['ci_95_lower'])} > 0"
            f"  AND  p = {stats['p_value_two_tailed']:.4f} < 0.05"
        )
        lines.append("     Candidate graduates to Champion status.")
    else:
        reasons = []
        if stats["ci_95_lower"] <= 0:
            reasons.append(f"CI_lower = {_fmt(stats['ci_95_lower'])} ≤ 0")
        if stats["p_value_two_tailed"] >= 0.05:
            reasons.append(f"p = {stats['p_value_two_tailed']:.4f} ≥ 0.05")
        lines.append(f"  ❌ HOLD: {' | '.join(reasons)}")
        lines.append("     Candidate stays in Candidate status.")
        lines.append("     Run more experiments or tune on nested CV only.")
    lines.append(BANNER)
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args():
    p = argparse.ArgumentParser(
        description="Multi-Seed Paired Statistical Evaluation Protocol",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument(
        "--matrix", required=True,
        help="Path to CSV with columns [seed, <baseline_col>, <candidate_col>]",
    )
    p.add_argument(
        "--baseline", default="baseline_auc",
        help="Column name for baseline AUC scores (default: baseline_auc)",
    )
    p.add_argument(
        "--candidate", default="candidate_auc",
        help="Column name for candidate AUC scores (default: candidate_auc)",
    )
    p.add_argument(
        "--seed-col", default="seed",
        help="Column name for seeds (default: seed)",
    )
    p.add_argument(
        "--json", action="store_true",
        help="Output full stats as JSON instead of human-readable report",
    )
    p.add_argument(
        "--append-log", metavar="LOG_PATH",
        help="Append the JSON result to this file (one object per line)",
    )
    return p.parse_args()


def load_matrix_pure(path: str, seed_col: str, baseline_col: str, candidate_col: str):
    """Pure-Python CSV reader as fallback when pandas is not available."""
    import csv
    seeds, baselines, candidates = [], [], []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            seeds.append(int(float(row[seed_col])))
            baselines.append(float(row[baseline_col]))
            candidates.append(float(row[candidate_col]))
    return seeds, baselines, candidates


def main():
    args = parse_args()

    matrix_path = Path(args.matrix)
    if not matrix_path.is_file():
        print(f"ERROR: matrix file not found: {matrix_path}", file=sys.stderr)
        sys.exit(2)

    # Load data
    try:
        if _SCIPY:  # scipy implies pandas
            df = pd.read_csv(matrix_path)
            seeds = df[args.seed_col].tolist()
            baselines = df[args.baseline].tolist()
            candidates = df[args.candidate].tolist()
        else:
            seeds, baselines, candidates = load_matrix_pure(
                str(matrix_path), args.seed_col, args.baseline, args.candidate
            )
    except KeyError as e:
        print(f"ERROR: missing column {e} in {matrix_path}", file=sys.stderr)
        sys.exit(2)

    deltas = [c - b for c, b in zip(candidates, baselines)]

    try:
        stats = compute_paired_stats(deltas)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(2)

    stats["seeds"] = seeds
    stats["deltas"] = deltas
    stats["baseline_col"] = args.baseline
    stats["candidate_col"] = args.candidate
    stats["matrix_path"] = str(matrix_path)

    if args.json:
        print(json.dumps(stats, indent=2))
    else:
        print(render_report(seeds, deltas, stats))

    # Optional: append to log file
    if args.append_log:
        log_path = Path(args.append_log)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(stats) + "\n")
        if not args.json:
            print(f"\n  📝 Result appended to: {log_path}")

    # Exit code signals promotion decision for CI pipeline integration
    sys.exit(0 if stats["promoted"] else 1)


if __name__ == "__main__":
    main()
