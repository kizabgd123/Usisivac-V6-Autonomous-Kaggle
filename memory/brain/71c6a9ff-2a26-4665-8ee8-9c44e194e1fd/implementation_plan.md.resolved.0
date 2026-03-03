# Implementation Plan - Heart Disease Elite Breach v3.2

This plan aims to push the Public LB score from 0.95339 to 0.9575+ by transforming the pipeline into a medical-aware architectural framework.

## Proposed Changes

### Preprocessing & Feature Engineering
- **MICE Imputation**: Use `sklearn.ensemble.IterativeImputer` to fill zero/missing cholesterol values.
- **ST_Slope Fix**: Map `ST_Slope` to ordinal values (1, 2, 3) for clinical alignment.
- **Ischemic Burden**: New feature `Oldpeak / (ST_Slope_ordinal + 0.1)`.
- **Age < 40 Cohort**: Surgical treatment of cholesterol zero-flags in young patients.
- **Redundancy Cleanup**: Ensure no overlapping features from previous iterations.

### Model Upgrades
- **XGBoost (DART)**: Re-enable DART booster with `rate_drop` for improved diversity.
- **LightGBM**: Reduce `num_leaves` and increase `reg_alpha/lambda` to prevent overfitting.
- **CatBoost**: tune `l2_leaf_reg` for stable convergence.
- **Multi-Seed Averaging**: Train over 3 seeds (42, 1337, 2024).

### Ensemble Strategy
- **Rank-Based Ensembling**: Average ranks of model predictions.
- **Nelder-Mead Optimization**: Optimize model weights on OOF Rank AUC.

## Verification Plan

### Automated Verification
Run `heart_top5_v3_2_elite.py` and verify:
1. **OOF AUC**: Must exceed 0.9555.
2. **Adversarial Validation**: Must remain < 0.52 (indicating train/test consistency).
3. **Submission Check**: Verify that `submission_heart_v3_2_elite.csv` is generated with correct ID range.

### Manual Verification
1. Review the logging output for weight distributions chosen by Nelder-Mead.
2. Compare final OOF score against v3 baseline.
