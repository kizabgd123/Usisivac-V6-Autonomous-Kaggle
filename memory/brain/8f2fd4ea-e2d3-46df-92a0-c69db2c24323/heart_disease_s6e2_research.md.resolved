# 📊 Heart Disease S6E2 — Top Tactics & Discussions

This report summarizes the most upvoted and effective tactics from the Kaggle competition **Playground Series S6E2: Predicting Heart Disease**.

## 🏆 Top Voted Discussions & Tactics

| Topic / Tactic | Upvotes | Key Result / Insight |
| :--- | :---: | :--- |
| **MLP with Linear & Periodic Embeddings** | 60 | **RealMLP** models are outperforming traditional GBDT models (XGB/LGB) as solo models. Periodic embeddings for numeric features capture non-linearities better than binning. |
| **The "Flipped Label" Trap** | 28 | Several rows in the dataset appear to have **flipped targets** (Presence vs Absence) based on physiological impossibility. Cleaning these can boost CV consistency. |
| **Thallium & Chest Pain TRAPS** | 12 | DO NOT treat these as pure numbers. They are categorical. Interactions like `ChestPainType * NumVessels` can be dangerous if the underlying integer mapping is arbitrary. |
| **Trust Your CV: Robust Ensemble** | 30 | High LB variance. A 10-fold Stratified CV with multiple seeds (Bagging) is mandatory. |
| **Model Explainability (SHAP)** | 47 | Identifies `NumVessels`, `Thallium`, and `ST_Slope` as the top 3 drivers. Over-weighting these in interactions might help. |
| **Increasing n_splits?** | 23 | Moving from 5-fold to 10-fold or even 20-fold shows marginal gains but significantly stabilizes the CV for blending. |

## 🧪 Top Voted Notebooks & Baselines

| Notebook Title | Upvotes | Tactic Highlight |
| :--- | :--- | :--- |
| **Heart\|XGB/LightGBM/CatB\|Baseline** | 119 | The standard "Triad" of GBDTs. Uses optimized hyperparameters for each. |
| **The best solo model: RealMLP** | 111 | **LB: 0.95397**. Uses a custom PyTorch MLP with periodic embeddings. This is currently the strongest "solo" architecture. |
| **❤️ CB&XGB\|Residual RF\|Feature Growth** | 75 | Uses "Residual RF" — training a Random Forest on the residuals of GBDTs. |
| **S6E2 \| CatB Only \| CV: 0.9555+** | 65 | Proves that a perfectly tuned CatBoost (with properly handled categorical indices) can beat complex ensembles. |

---

## 🔍 Gap Analysis: V10.13 vs SOTA

| Feature | V10.13 Status | SOTA Recommendation |
| :--- | :---: | :--- |
| **Numerical Embeddings** | ❌ None (uses raw/scaled) | Implement **Periodic Embeddings** for MLP (Phase 3 candidate). |
| **Label Noise** | ❌ None | Apply **Flipped Label filter** (identify rows where target=1 but risk=0). |
| **Categorical Traps** | ⚠️ Partial | Ensure `Thallium` and `ChestPain` are NEVER multiplied as ranks; use OHE or pure CatBoost indices. |
| **Ensemble Logic** | ✅ Stacking + Blend | Current stacking is strong, but needs **RealMLP** integration. |

---

## 🚀 Recommendation for V10.14

1.  **Drop Arbitrary Rank Multiplications**: Change `PainVes` and `AngHR` to interaction categories rather than numerical multiplications.
2.  **Flipped Label Scrubbing**: Add a preprocessing step to detect high-confidence "outliers" (e.g., target=1 but extremely low Risk Score) and potentially remove them from training.
3.  **RealMLP Prototype**: Move from `MLPClassifier` to a custom PyTorch MLP if performance stalls.
4.  **10-Fold Bagging**: Increase `N_FOLDS` to 10 for the final submission to match the top strategy.
