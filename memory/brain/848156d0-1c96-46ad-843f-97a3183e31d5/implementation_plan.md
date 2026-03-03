# Implementation Plan: Heart Disease Kaggle CPU Pipeline (v3.7 Elite Calibration)

The goal is to implement "Grandmaster Hardening" parameters to significantly improve the heart disease prediction model's AUC score, aiming for 0.9575+. This involves correcting the `ischemic_burden` formula, implementing a 10-fold CV strategy, and applying advanced regularization to XGBoost and LightGBM.

## Proposed Changes

### [Component] Data Pipeline

#### [MODIFY] [heart-disease-s6e2-elite-breach-v32-cpu.ipynb](file:///home/kizabgd/Desktop/Istrazivanje/heart_disease/kaggle_push_cpu/heart-disease-s6e2-elite-breach-v32-cpu.ipynb)

- **Advanced Preprocessing (Elite Breach v3.2)**:
    - **Surgical Cholesterol Treatment**: Add `chol_zero_flag` and `chol_zero_flag_x_Age` interaction; treat 0 as NaN.
    - **MICE Imputation**: Use `IterativeImputer` to preserve biological correlations.
    - **Ratio-based Ischemic Burden**: `ST depression / (Slope of ST + 0.1)`.
    - **Trinity Medical Features**: Add `pulse_pressure`, `cv_age_acceleration`, and `metabolic_proxy`.
- **10-Fold Cross-Validation**: Implement 10-fold CV with OOF prediction tracking.
- **XGBoost Hardening**: 
    - `booster='dart'`, `learning_rate=0.01`, `max_depth=6`.
- **LightGBM Hardening**:
    - `min_data_in_leaf=30`, `reg_alpha=0.1`, `reg_lambda=0.1`, `feature_fraction=0.8`.
- **Ensemble Strategy**: Rank Blending with power calibration and OOF verification.


## Verification Plan

### Automated Tests
- **Pre-flight Check**: Run the first 2 folds locally to ensure no OOM or device errors.
- **OOF AUC Check**: Verify that the local OOF AUC is > 0.9570.

### Manual Verification
- **Kaggle Push**: Run `kaggle kernels push -p heart_disease/kaggle_push_cpu` and monitor for AUC improvement.
