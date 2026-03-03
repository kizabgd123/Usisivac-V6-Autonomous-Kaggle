# Implementation Plan: Bidding V10 \"Zenith\"

Objective: Surpass V6 (0.3980) and target 1st place (< 0.2750).

## User Review Required
> [!IMPORTANT]
> V10 will use **Pseudo-Labeling** from the V6 0.398 submission to provide signal from the 2025 test distribution. It also incorporates **In-fold Target Encoding** and **Contractor Style Clustering**.

## Proposed Changes

### [1] Data Augmentation
- Read `submission_v6_elite.csv`.
- Augment train data with Top 1000 samples from the test set using V6 predictions as targets.

### [2] Advanced Feature Set
- **V6 Legacy**: `item_count`, `cat_unique`, `unit_unique`, `quant_sum`, `quant_mean`, `inflation_idx`.
- **Baseline Estimate**: `log1p(est_amt_sum)` (Median Unit Price logic).
- **Temporal Dynamics**: `days_since_bid` (Contractor's bidding frequency).
- **Competition**: `num_bidders` for the job id.
- **Contractor DNA**: Refined multiplier statistics.
- **Clustering**: K-Means clustering of contractors based on volume and average bid size.

### [3] Modeling & Calibration
- Target: `log1p(total_bid)`.
- Base Models: XGBoost, LightGBM, CatBoost (5-seed average).
- Stacking: Ridge meta-learner on 2024 holdout.
- **Calibration**: Isotonic Regression to adjust prediction scale.

## Verification Plan
- Target Holdout RMSLE (2024): < 0.30.
- Public LB goal: < 0.35.
