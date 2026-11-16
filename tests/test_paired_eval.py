import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from eval.paired_eval import (
    CANONICAL_SEEDS, EvaluationError, PromotionBlocked, append_eval_history,
    evaluate_paired_scores, guarded_promote, require_promote,
)
from eval.run_eval import run_multiseed_evaluation
from eval.promote_artifacts import promote_artifacts


def test_paired_gate_promotes_only_strong_consistent_delta():
    baseline = {seed: 0.90 for seed in CANONICAL_SEEDS}
    candidate = {seed: 0.90 + delta for seed, delta in zip(CANONICAL_SEEDS, [0.0020, 0.0030, 0.0025, 0.0024, 0.0028])}
    report = evaluate_paired_scores(baseline, candidate)
    assert report["summary"]["verdict"] == "PROMOTE"
    assert report["summary"]["p_value"] < 0.05
    assert report["summary"]["ci_lower"] > 0
    require_promote(report)


def test_noisy_small_delta_is_hold():
    report = evaluate_paired_scores([0.9] * 5, [0.900372, 0.901, 0.899, 0.9001, 0.9002])
    assert report["summary"]["verdict"] == "HOLD"
    with pytest.raises(PromotionBlocked):
        require_promote(report)


def test_zero_variance_fails_closed():
    report = evaluate_paired_scores([0.9] * 5, [0.91] * 5)
    assert report["summary"]["p_value"] == 1.0
    assert report["summary"]["verdict"] == "HOLD"


def test_requires_canonical_seeds_and_finite_auc():
    with pytest.raises(EvaluationError):
        evaluate_paired_scores([0.9] * 5, [0.91] * 5, seeds=[1, 2, 3, 4, 5])
    with pytest.raises(EvaluationError):
        evaluate_paired_scores([0.9] * 5, [0.91, 0.91, np.nan, 0.91, 0.91])


def test_promotion_callback_is_not_called_for_hold():
    calls = []
    hold = evaluate_paired_scores([0.9] * 5, [0.9001, 0.8999, 0.9002, 0.9, 0.9001])
    with pytest.raises(PromotionBlocked):
        guarded_promote(hold, lambda: calls.append("promote"))
    assert calls == []


def test_history_is_append_only_jsonl(tmp_path):
    report = evaluate_paired_scores([0.9] * 5, [0.902, 0.903, 0.9025, 0.9024, 0.9028])
    log = tmp_path / "eval" / "eval_history.jsonl"
    append_eval_history(report, log)
    append_eval_history(report, log)
    lines = log.read_text().splitlines()
    assert len(lines) == 2
    assert len(json.loads(lines[0])["evaluation_matrix"]) == 5
    assert "runtime_environment" in json.loads(lines[0])


def test_run_eval_uses_same_folds_and_complete_oof_predictions():
    rng = np.random.default_rng(7)
    target = np.array([0, 1] * 50)
    frame = pd.DataFrame({"signal": target + rng.normal(0, 0.2, 100), "target": target})
    calls = []

    def adapter(X_train, y_train, X_valid, *, seed, fold):
        calls.append((seed, fold, len(X_train), len(X_valid)))
        p = 1 / (1 + np.exp(-X_valid["signal"].to_numpy()))
        return {"baseline": p, "candidate": p.copy()}

    plan = {"evaluation": {"seeds": list(CANONICAL_SEEDS), "n_splits": 5, "metric": "roc_auc", "alpha": 0.05, "confidence_level": 0.95}}
    report = run_multiseed_evaluation(frame, "target", adapter, plan=plan)
    assert len(calls) == 25
    assert report["seeds"] == list(CANONICAL_SEEDS)
    assert report["summary"]["verdict"] == "HOLD"


def test_target_encoding_fold_prior_does_not_leak(monkeypatch):
    from Usisivac.src.agents import target_encoding

    plan = Path(target_encoding.__file__).resolve().parents[3] / "eval" / "experiment_plan.json"
    monkeypatch.setenv("USISIVAC_EXPERIMENT_PLAN", str(plan))
    categories = pd.Series([f"cat-{i}" for i in range(20)], name="category")
    labels = pd.Series([0] * 6 + [1] * 14, name="target")
    encoded, _, _, _ = target_encoding.target_encode_feature(categories, labels, n_splits=5, smoothing=1.0, random_state=7)
    expected = np.empty(20)
    from sklearn.model_selection import StratifiedKFold
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=7)
    for train_idx, valid_idx in cv.split(categories, labels):
        expected[valid_idx] = labels.iloc[train_idx].mean()
    np.testing.assert_allclose(encoded.to_numpy(), expected)


def test_target_encoder_rejects_unregistered_smoothing(monkeypatch):
    from Usisivac.src.agents import target_encoding

    plan = Path(target_encoding.__file__).resolve().parents[3] / "eval" / "experiment_plan.json"
    monkeypatch.setenv("USISIVAC_EXPERIMENT_PLAN", str(plan))
    categories = pd.Series(["a", "b"] * 10)
    labels = pd.Series([0, 1] * 10)
    with pytest.raises(ValueError, match="not pre-registered"):
        target_encoding.target_encode_feature(categories, labels, smoothing=2.0)


def test_summary_tampering_is_blocked():
    report = evaluate_paired_scores([0.9] * 5, [0.902, 0.903, 0.9025, 0.9024, 0.9028])
    report["summary"]["verdict"] = "PROMOTE"
    report["summary"]["p_value"] = 0.0001
    with pytest.raises(PromotionBlocked):
        require_promote(report)


def test_artifact_copy_is_guarded(tmp_path):
    candidate = tmp_path / "candidate.pkl"
    champion = tmp_path / "champion.pkl"
    candidate.write_bytes(b"candidate")
    champion.write_bytes(b"old")
    hold = evaluate_paired_scores([0.9] * 5, [0.9001, 0.8999, 0.9002, 0.9, 0.9001])
    hold_report = tmp_path / "hold.json"
    hold_report.write_text(json.dumps(hold))
    with pytest.raises(PromotionBlocked):
        promote_artifacts(hold_report, [(candidate, champion)])
    assert champion.read_bytes() == b"old"

    promote = evaluate_paired_scores([0.9] * 5, [0.902, 0.903, 0.9025, 0.9024, 0.9028])
    promote_report = tmp_path / "promote.json"
    promote_report.write_text(json.dumps(promote))
    assert promote_artifacts(promote_report, [(candidate, champion)]) == [champion]
    assert champion.read_bytes() == b"candidate"
