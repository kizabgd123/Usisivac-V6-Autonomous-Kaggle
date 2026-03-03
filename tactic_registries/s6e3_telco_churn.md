# Tactic Registry: Kaggle S6E3 Telco Churn

## 🏛️ Project Constitution Alignment
- **Domain**: Telco (Transactional & Service-based)
- **Metric**: ROC AUC (Optimization focus)
- **Target**: `Churn` (Binary)

## 🧪 Golden Recipe (Thesis Phase)
1. **Numeric Transformation**: `TotalCharges` conversion is non-negotiable (contains empty strings).
2. **Service Enrichment**: `Service_Diversity` (sum of 'Yes' in service cols) and `Contract_Type` encoding.
3. **Imbalance Awareness**: SMOTE-ENN or Class Weights required if churn occurs in <20% of samples.
4. **Baseline Model**: GBDT Ensemble (CatBoost > XGBoost >= LightGBM).

## ⚠️ Anti-Patterns
- Handling `TotalCharges` as categorical.
- Ignoring the `tenure`-`Contract` interaction.
- Over-fitting on `customerID` (drop it).

## 📊 Effectiveness Scoring
- Baseline ROC AUC Target: >0.88 (Top-tier local CV).
