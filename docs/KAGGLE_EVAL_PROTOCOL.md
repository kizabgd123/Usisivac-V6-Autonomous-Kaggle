# Kaggle Multi-Seed Evaluation Protocol

Enforces statistical rigor in machine learning competition iterations and autonomous modeling by requiring a **Multi-Seed Paired t-Test** with 95% Confidence Interval before any model candidate can be promoted to Champion status.

---

## 1. Champion Promotion Gate

A model **MUST NOT** be promoted from **Candidate** to **Champion** status unless **ALL** of the following conditions are met:

1. **Multi-Seed Evaluation Completed**: Out-of-Fold (OOF) AUC scores collected for all 5 canonical seeds:
   ```python
   SEEDS = [42, 43, 44, 45, 46]
   ```
   Both the baseline and candidate models must evaluate across identical `StratifiedKFold` splits per seed.
2. **Paired t-Test Passed**: Two-tailed $p$-value is strictly less than 0.05:
   $$p < 0.05$$
3. **95% Confidence Interval Strictly Positive**: The lower bound of the 95% confidence interval for the mean delta ($\text{CI}_{\text{lower}}$) is strictly greater than zero:
   $$\text{CI}_{\text{lower}} > 0$$

Both conditions (2 and 3) must hold simultaneously. The runner must execute `eval/paired_eval.py` (or `python eval/run_eval.py paired-eval`) and yield an explicit `PROMOTE` verdict (exit code 0).

---

## 2. Target Encoding Regularization Policy

The smoothing parameter $m$ (or any regularization hyperparameter for target encoding) must be either:

- **Pre-registered**: Explicitly declared in the experiment plan prior to any cross-validation runs, OR
- **Inner-Fold Optimized**: Tuned exclusively inside a nested inner-fold cross-validation on the training split only.

> [!CAUTION]
> Selecting or tuning $m$ based on validation fold AUC constitutes target leakage and invalidates the experiment. Any experiment violating this policy must be rejected and re-run under a compliant configuration.

---

## 3. Cross-Environment Artifact Policy

- Prediction artifact hash fingerprints (MD5/SHA256 of Parquet/CSV files) **MUST NOT** be compared across differing runtime environments (e.g. local CPU vs. Kaggle kernel).
- Divergences arise naturally from LightGBM thread scheduling non-determinism, pyarrow version variations, and CPU floating-point architecture.
- The **only valid comparison** is metric AUC computed deterministically in the same runtime environment.

---

## 4. Statistical Reporting Requirement

Every evaluation run must log its full statistical summary to the shared log (`eval/eval_history.jsonl`):

- Mean delta ($\bar{d}$)
- Corrected sample standard deviation ($s_d$)
- $t$-statistic
- Two-tailed $p$-value
- 95% Confidence Interval bounds $[\text{CI}_{\text{lower}}, \text{CI}_{\text{upper}}]$
- Explicit promotion verdict (`PROMOTE` / `HOLD`)
- Evaluated seeds `[42, 43, 44, 45, 46]`
- Execution environment name

---

## 5. CLI Usage Examples

### Running Paired Evaluation via `eval/run_eval.py`
```bash
python eval/run_eval.py paired-eval \
    --matrix eval/datasets/sample_eval_matrix.csv \
    --baseline baseline_auc \
    --candidate candidate_auc \
    --append-log eval/eval_history.jsonl
```

### Running Standalone `paired_eval.py`
```bash
python eval/paired_eval.py \
    --matrix eval/datasets/sample_eval_matrix.csv \
    --json
```

### Exit Codes
- `0`: Model meets criteria and is approved for **PROMOTE**
- `1`: Model fails criteria; decision is **HOLD**
- `2`: Matrix format error or missing arguments
