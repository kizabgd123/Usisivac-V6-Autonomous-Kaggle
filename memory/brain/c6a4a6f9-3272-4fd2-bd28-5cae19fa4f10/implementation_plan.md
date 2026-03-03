# Feature Selection & Noise Reduction Plan

We will perform comprehensive feature selection on the Heart Disease dataset to mitigate the curse of dimensionality, remove noise, and extract robust predictive signals.

## User Review Required
> [!WARNING]
> The requested datasets are located in `/root/.cache/...`. The Python script we create will need sufficient permissions to read from `/root`. You must either run the generated script with `sudo` or verify that the user `kizabgd` has read access to those files.

## Proposed Changes

We will implement a Python script to execute the 4-stage feature selection pipeline and visualize the impact.

### Feature Selection Pipeline
- **Noise & Variance Detection:** Remove features with zero or near-zero variance using `sklearn.feature_selection.VarianceThreshold`.
- **Mutual Information Scoring:** Calculate non-linear dependency with `mutual_info_classif` to identify and retain features with high predictive power.
- **Permutation Importance:** Train a baseline LightGBM/XGBoost model, then use `sklearn.inspection.permutation_importance` to shuffle features and measure the drop in performance, isolating true signals.
- **Golden Features Extraction:** Intersect the most valuable features from both MI and Permutation Importance tests to build the final list of "Golden Features".

### Components

---

#### [NEW] [feature_selection.py](file:///home/kizabgd/Desktop/Istrazivanje/scripts/feature_selection.py)
This script will:
1. Load `train.csv` and `test.csv` from the specified Kagglehub cache path.
2. Run identical preprocessing to handle any missing values or categorical features.
3. Compute Variance, MI, and Permutation Importance.
4. Train baseline models (using Stratified K-Fold CV) on both the full feature set and the reduced "Golden Features" set.
5. Generate and save `feature_impact.png` plotting the ROC curves.
6. Export the final `golden_features.json` list to disk for future use.

## Verification Plan

### Automated Tests
We will run `python scripts/feature_selection.py` to ensure it completes successfully and produces the expected `golden_features.json` and `feature_impact.png` outputs.

### Manual Verification
Review the generated `feature_impact.png` to confirm that the Golden Features model maintains or improves ROC-AUC performance compared to the baseline model with all features, thus proving successful noise reduction.
