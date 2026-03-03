# Goal Description

The goal is to upgrade the Kaggle pipeline for the Heart Disease (S6E2) competition to a new version (v10.0) that aims to break the 0.9400 AUC barrier while also executing faster than the current v9.2 script.

## Proposed Changes (V10.1 Turbo)

The script must be entirely self-contained for a Kaggle Notebook and highly optimized for speed to offset the cost of Pseudo-Labeling.

### 1. Data Processing
#### [MODIFY] `heart_pipeline_v10.py`
- Add `RobustScaler` after MICE imputation to handle outliers before feeding data to models (as recommended in elite scripts).
- Keep MICE and advanced elite features.

### 2. Speed Optimizations
- Reduce `N_FOLDS` to 4.
- Reduce `SEEDS` to [42] (Single seed, heavily relying on Pseudo-Labeling for stability).
- Maintain only GPU-accelerated models (XGB DART, LGBM GOSS, CatBoost). Drop CPU models like HistGB to dramatically speed up execution.
- Lower total boosting rounds to ~1500 with `early_stopping=100`.

### 3. Stacking & Pseudo-Labeling Loop
- Replace `LogisticRegression` with `RidgeClassifier` as the Level-2 Meta-Learner to prevent rank/probability overfitting.
- Implement **Recirculation Loop (Pseudo-Labeling)**: After Phase 1 stacking, identify `test` samples with >98.5% and <1.5% confidence. Combine these with the original training set as hard labels (1 and 0), then rerun the **entire** stacking pipeline (Phase 2).


Currently, v9.2 uses a basic feature engineering setup, `-1` imputation for missing cholesterol, and a slow 10-fold CV with 3 seeds across XGBoost, LightGBM, and CatBoost. It ensembles them using a simple rank-based weighted average.

The new `heart_pipeline_v10.py` will introduce the following "Grandmaster" strategies identified from top-performing scripts:

### [NEW] `heart_pipeline_v10.py`
A new script will be created with the following upgrades:
1. **Speed Optimizations**:
    - Reduce to 5 Folds and 2 Seeds (10 fits per model instead of 30) for much faster execution.
    - Reduce CatBoost rounds slightly or use early stopping more aggressively.
    - Introduce `HistGradientBoostingClassifier` as it is extremely fast and provides good diversity.
2. **Advanced Imputation (MICE)**:
    - Instead of filling zeros/missing values with `-1` or median, use `IterativeImputer` to predict the missing cholesterol values based on other clinical features.
3. **Medical-Aware Feature Engineering**:
    - `Ischemic_Burden`: `Oldpeak / (ST_Slope_Ordinal + 0.1)`
    - `Young_Signal`: Identify patients under 40 with missing cholesterol.
    - `CardioRisk_Score`: A weighted sum of age, sex, cholesterol, and resting BP.
    - `BP_Chol_ratio`, `Age_MaxHR`, `HR_Reserve`, `Pain_Vessels`.
4. **Strict Deduplication**:
    - When merging the original `Heart_disease_statlog.csv` dataset, drop duplicates strictly on feature columns to prevent data leakage.
5. **Level-2 Meta-Learner (Stacking)**:
    - Replace the manual rank blend with a robust `LogisticRegression` meta-learner trained on the Out-Of-Fold (OOF) predictions of the Level-1 models (XGB, LGB, CAT, HGB, ET).

## Verification Plan

### Automated Tests
- Run the new `heart_pipeline_v10.py` script locally on the GPU.
- Verify that the execution time is shorter than v9.2.
- Verify that the OOF AUC score is >0.9400.

### Manual Verification
- After successful local execution, I will use the Kaggle CLI tools to submit the generated `submission_v10.0.csv` file up to the Kaggle leaderboard to confirm the actual public score. This will be the ultimate validation of the strategy.
