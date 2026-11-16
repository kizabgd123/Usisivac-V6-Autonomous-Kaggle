# Paired multi-seed evaluation and Champion gate

This directory implements the protocol requested in Issue #7. The original repository did not contain a model evaluation entry point or a Champion checkpoint writer, so model training is supplied through a small fold adapter and all Champion artifact replacement is routed through the promotion guard.

## Protocol

- Canonical seeds are fixed to `42, 43, 44, 45, 46`.
- Each seed uses `StratifiedKFold(n_splits=5, shuffle=True, random_state=seed)`.
- The adapter receives one training/validation split and must fit both baseline and candidate using the same training rows. It returns both validation probability vectors in that same call.
- Exactly one OOF prediction per training row is required for each model and seed. AUC is calculated once per model per seed.
- The statistical unit is the five paired seed-level AUC deltas (candidate minus baseline). The gate uses a two-sided paired Student t-test and a two-sided 95% t confidence interval with sample standard deviation (`ddof=1`).
- Promotion requires both `p_value < 0.05` and `ci_lower > 0`. Invalid inputs and degenerate zero-variance deltas fail closed as `HOLD`.
- Every run appends the evaluation matrix, summary, seeds, timestamp and runtime environment to `eval/eval_history.jsonl`. The latest report is written to `eval/latest_eval.json`.

## Model adapter

Create an importable function, for example `project/eval_adapter.py`:

```python
def fit_predict_fold(X_train, y_train, X_valid, *, seed: int, fold: int):
    # Fit preprocessing and both estimators on X_train / y_train only.
    baseline = make_baseline(seed=seed, fold=fold)
    candidate = make_candidate(seed=seed, fold=fold)
    baseline.fit(X_train, y_train)
    candidate.fit(X_train, y_train)
    return {
        "baseline": baseline.predict_proba(X_valid)[:, 1],
        "candidate": candidate.predict_proba(X_valid)[:, 1],
    }
```

Run the evaluator:

```bash
python eval/run_eval.py \
  --data data/train.csv \
  --target Churn \
  --evaluator project.eval_adapter:fit_predict_fold
```

Adapter-side preprocessing, feature selection, imputation and encoding must be fitted on the fold training partition only. Validation AUC must not be used to choose hyperparameters.

## Champion promotion

Never copy candidate checkpoints directly over baseline or Champion files. After evaluation, use the guard:

```bash
python eval/promote_artifacts.py \
  --report eval/latest_eval.json \
  --artifact artifacts/candidate_model.pkl=artifacts/champion_model.pkl
```

The guard recomputes the test from the persisted score matrix and verifies the recorded summary before staging/replacing files. A `HOLD`, malformed report, missing candidate file or mismatch blocks promotion. Files are staged before replacement; each destination replacement is atomic on its filesystem.

The repository did not previously contain a Champion writer or baseline artifact update path. This CLI is therefore the supported promotion entry point for future model pipelines; existing code should not bypass it.

## Target encoding regularization

`experiment_plan.json` pre-registers `smoothing=1.0`. The target encoder rejects any different value unless the plan itself is deliberately changed and committed before outer evaluation. Outer-fold OOF category statistics and the smoothing prior are computed exclusively from that fold's training partition. Inner-fold tuning is not currently implemented; the pre-registered policy is the supported path.

Prediction-file hashes are not compared across different runtime environments. Baseline and candidate metrics are paired inside the same run; runtime metadata is stored for auditability.

## Statistical caveat

The requested t-test has five observations (df=4), one per seed. It implements the issue's required decision rule but is not a replacement for a larger independent holdout or repeated-experiment design.
