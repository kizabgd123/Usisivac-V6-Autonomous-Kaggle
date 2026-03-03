# Implementation Plan - Heart Disease Elite Baseline (v3.16)

Address the Rule 42/38/39 constitutional warnings by implementing a scientifically backed baseline for the S6E2 competition.

## 1. Feature Engineering (Scientific Guard)

### Rule 38: Tanaka Formula
- Replace `220 - Age` with `208 - 0.7 * Age` for `HR_Pct` and `HR_Reserve`.
- Add `Ischemic Burden` interaction: `Oldpeak * Exercise_Angina`.

### Rule 39: Oldpeak Normalization
- Transformation: `Log1p` -> `Outlier Clipping (99th percentile)` -> `Z-score Standardization`.

## 2. Model Diversity (Rule 33 & 44)

### Rule 42: UCI Target Stats
- Instead of `pd.concat`, we will calculate `target_mean` and `target_std` per `Sex/AgeGroup` from the UCI set.
- Map these statistics back to the synthetic Training/Test sets as high-level Bayesian priors.

### Rule 33: Golden Recipe Ensemble
- Implement `XGBRegressor` + `LGBMRegressor` + `CatBoostRegressor`.
- 5-fold Stratified CV.
- Multi-seed averaging (5 seeds).

## 3. Verification Plan

- Check `GUARD_ALERT.json` for validation.
- Verify OOF AUC is within the 0.955-0.957 optimal range (Rule 32).
- Ensure no direct concatenation of UCI data in the training loop.
