import sys
import os
import pytest
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from eval.paired_eval import compute_paired_stats, load_matrix_pure


def test_compute_paired_stats_promote():
    # Significant improvement across all 5 canonical seeds
    deltas = [+0.0020, +0.0019, +0.0022, +0.0018, +0.0021]
    stats = compute_paired_stats(deltas)
    assert stats["promoted"] is True
    assert stats["mean_delta"] > 0
    assert stats["ci_95_lower"] > 0
    assert stats["p_value_two_tailed"] < 0.05


def test_compute_paired_stats_hold_on_noise():
    # Small delta with high variance (S6E11 real example: p ≈ 0.34)
    # Mean delta ~ +0.000372, but not statistically significant
    deltas = [+0.000372, -0.000100, +0.000900, -0.000200, +0.000888]
    stats = compute_paired_stats(deltas)
    assert stats["promoted"] is False
    assert stats["p_value_two_tailed"] >= 0.05 or stats["ci_95_lower"] <= 0


def test_compute_paired_stats_hold_on_negative():
    # Model degradation
    deltas = [-0.0010, -0.0020, -0.0015, -0.0005, -0.0012]
    stats = compute_paired_stats(deltas)
    assert stats["promoted"] is False
    assert stats["ci_95_lower"] <= 0


def test_load_matrix_pure():
    sample_csv = PROJECT_ROOT / "eval" / "datasets" / "sample_eval_matrix.csv"
    seeds, baselines, candidates = load_matrix_pure(
        str(sample_csv),
        seed_col="seed",
        baseline_col="baseline_auc",
        candidate_col="candidate_auc",
    )
    assert len(seeds) == 5
    assert seeds == [42, 43, 44, 45, 46]
    assert len(baselines) == 5
    assert len(candidates) == 5
