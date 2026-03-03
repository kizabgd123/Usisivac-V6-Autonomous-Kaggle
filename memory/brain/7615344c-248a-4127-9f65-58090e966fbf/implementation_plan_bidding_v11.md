# Implementation Plan: Bidding V11 "Genesis" (KILLSHOT)

Objective: Surpass 1st place benchmark (< 0.275 LB) using high-precision Multiplier Prediction and Bayesian Item Priors.

## Proposed Strategy: "The Multiplier Bridge"

Instead of predicting the raw bid amount, we predict the contractor's **relative markup** compared to a highly robust "Market Price" baseline.

### 1. Bayesian Item Prices [NEW]
- Compute `unit_price` as `amount / quantity`.
- Create a Bayesian Prior for every `pay_item_id`: `price = (count * median + k * global_median) / (count + k)`.
- This ensures rare items don't skew the estimate with outliers.

### 2. Primary Target: The Multiplier [CRITICAL]
- `Market_Estimate = Sum(Item_Quantity * Bayesian_Prior_Price)`
- `Target = total_bid / Market_Estimate`
- We will model `log(Target)` because it is symmetric and stable.

### 3. Contractor "Signature" Features
- **Markup Bias**: Median historical multiplier.
- **Strategic Volatility**: Standard deviation of their markup.
- **Category Affinity**: Difference between their markup in "BRIDGE" vs "ASPHALT".

### 4. Advanced Ensemble & Calibration
- 5-Fold Stratified CV on `log(Target)`.
- Stack: XGBoost (DART) + LightGBM + CatBoost.
- **Post-Processing**: Clipped Isotonic Regression to ensure monotonic alignment with Public LB density.

## Verification Plan
1. **Local CV**: Target Holdout RMSLE < 0.30.
2. **Feature Importance Check**: verify if "Bayesian Estimate" is the dominant signal.
3. **Kaggle Submission**: Final verification on Public LB.
