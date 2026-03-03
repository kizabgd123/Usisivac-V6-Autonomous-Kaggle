# Knowledge Item: Heart Disease S6E2 Elite Strategy

This KI documents the "Elite Breach" strategy for the Heart Disease Prediction competition (S6E2), focusing on the implementation details that led to top-tier scores.

## 核心 Strategy: Pseudo-Labeling Boost

The core of the strategy is a two-stage training process utilizing high-confidence test predictions.

### Stage 1: Initial Blend
- **Models**: CatBoost (multi-seed) + LightGBM.
- **Goal**: Generate initial probabilities for the test set.
- **Blending**: Optimal alpha search (weighted average) based on OOF (Out-Of-Fold) AUC.

### Stage 2: Pseudo-Labeling
- **Threshold**: `high_conf = 0.95` (predictions above 0.95 or below 0.05).
- **Augmentation**: High-confidence test samples are added to the training set with their predicted labels.
- **Retraining**: Models are retrained on the augmented dataset (`X_tr_aug`, `y_aug`).

## Feature Engineering (FE)

The strategy relies heavily on domain-specific medical features and robust preprocessing.

### 1. Medical Domain Features
- **RPP (Rate Pressure Product)**: `MaxHR * RestingBP / 100`.
- **Framingham Risk Score (Simplified)**: A weighted sum of Age, Cholesterol, Blood Pressure, Sex, and Angina.
- **Ischemic Index**: `Oldpeak / (ST_Slope_Ord + 0.1)`.
- **HR Reserve & Pct**: Calculations relative to the theoretical max heart rate (`220 - Age`).
- **Thallium One-Hot**: Flags for Fixed, Normal, and Reversible defects.

### 2. Preprocessing & Mapping
- **Cholesterol Imputation**: Medians grouped by `Sex` and `AgeBin`.
- **Global Maps (Target Encoding)**: Smoothed target encoding for categorical columns to capture nonlinear signals.
- **KBins**: Binning numerical features into fixed intervals (e.g., 20 bins).
- **Robust Scaling**: Using Median and IQR to handle outliers in medical data.

## Model Configuration

### CatBoost
- **Iterations**: 4000 (CPU) or 6000 (GPU).
- **Class Weights**: `Balanced` (critical for heart disease datasets which are often imbalanced).
- **Metric**: `AUC`.

### LightGBM
- **Hyperparameters**: `num_leaves=31`, `learning_rate=0.05`, `subsample=0.8`, `colsample_bytree=0.8`.
- **Boosting**: Standard GBDT with early stopping.

## Expected Results
- **OOF AUC**: `0.9558 - 0.9562+`.
- **Stability**: Multi-seed averaging (CatBoost) significantly reduces variance.

> [!TIP]
> Use `HAS_GPU` detection to automatically scale iterations and utilize faster training if `nvidia-smi` is detected.
