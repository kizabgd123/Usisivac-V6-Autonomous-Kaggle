# Usisivac: Academic & ML Research - Kaggle S6E3

## 1. Domain Science: The Mechanics of Churn
Churn prediction is not just a classification problem; it's a dynamic behavioral study. In the context of Telco data (implied by features like `StreamingTV`, `TechSupport`, `Contract`):
- **Contractual vs. Non-Contractual Churn:** The presence of `Contract` (Month-to-month, Two year) indicates a contractual relationship where churn is a discrete event (termination).
- **Service Quality vs. Price Sensitivity:** Features like `Fiber optic` and `MonthlyCharges` vs. `TechSupport` suggest a trade-off between perceived value and cost.
- **Academic Insight:** Research from 2025-2026 emphasizes **Profit-Driven Churn Modeling**. Instead of just predicting *who* will leave, models should focus on *which* customers are profitable to retain (ProfTree, financial integration).

## 2. State-of-the-Art ML Approaches (2025-2026)
- **Primary Algorithms:** 
    - **CatBoost:** Superior for categorical features (gender, PaymentMethod, InternetService) without extensive preprocessing.
    - **XGBoost & LightGBM:** Standard for high-performance tabular learning.
    - **TabNet:** Useful for deep learning on tabular data, though ensembles usually win.
- **Handling Imbalance (Crucial):**
    - **SMOTE-ENN / Borderline-SMOTE:** Advanced resampling to clean boundaries between classes.
    - **Cost-Sensitive Learning:** Adjusting weights in gradient boosters to penalize missing churners more than false positives.
- **Explainable AI (XAI):**
    - **SHAP (SHapley Additive exPlanations):** Essential for understanding feature importance at a per-customer level.
    - **LIME:** For local interpretability.

## 3. Challenge Specifics (S6E3)
- **Metric:** ROC AUC (Area Under the Receiver Operating Characteristic).
- **Strategy:**
    1. **Pre-processing:** Handle `TotalCharges` carefully (often contains hidden strings or needs numeric conversion). Transform `tenure` (log-transform or binning).
    2. **Feature Engineering:** Create `Ratio_Charges` (Monthly/Total), `Service_Diversity` (Count of 'Yes' in service columns).
    3. **Ensemble:** A 3-way blend of CatBoost, XGBoost, and LightGBM is the "Grandmaster" baseline.
    4. **Calibration:** Use Isotonic Regression or Platt Scaling to ensure predicted probabilities are reliable for ROC AUC.

---
*Research conducted by Usisivac Node*
