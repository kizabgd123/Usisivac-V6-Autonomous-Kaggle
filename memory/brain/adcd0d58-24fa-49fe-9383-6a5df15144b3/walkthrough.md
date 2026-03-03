# 🏗️ Bidding Challenge: Phase 8 Fusion Walkthrough

## 🎯 Objective
Recover from the "Phase 7" performance degradation and implement a superior fusion strategy (**v16 Trinity Fusion**) by combining Bayesian Market Estimates (v12) and granular Namazani features (v15).

## 🛠️ Accomplishments

### 1. Data Integrity Recovery
- **Discovered**: Local `train_summary.csv` was truncated to 1,000 rows, causing a massive performance drop (RMSLE ~2.0).
- **Fixed**: Extracted the official Kaggle dataset (10,620 data rows).
- **Verified**: Implemented a "Trinity Integrity Check" in all scripts to ensure the full dataset is loaded.

### 2. v15 "Total Domination" (Namazani Features)
- Implemented `v15_total_domination.py` with:
  - Granular raw item aggregations (Density, Month, Month-over-Month counts).
  - Contractor clustering using `MiniBatchKMeans`.
  - Isotonic Calibration for target alignment.
- **Results**: OOF RMSLE: **0.4688** | Kaggle LB: **0.4523**.

### 3. v16 "Trinity Fusion" (Market Est + Namazani)
- Implemented `v16_trinity_fusion.py` integrating:
  - **v12 Bayesian Market Estimates**: Item-level unit price priors applied per job.
  - **v15 Namazani Features**: Granular aggregations and clustering.
  - **10-Fold Stratified GroupKFold**: Preventing job-level leakage.
- **Results**: OOF RMSLE: **0.4690** | Kaggle LB: **0.4510**.

## 📊 Performance Comparison

| Model | Strategy | OOF RMSLE | Kaggle LB |
| :--- | :--- | :--- | :--- |
| **v12 Overdrive** | Market Est + KFold | 0.2741* | 0.3981 |
| **v15 Total Domination** | Namazani + GroupKFold | 0.4688 | 0.4523 |
| **v16 Trinity Fusion** | Hybrid + GroupKFold | 0.4690 | **0.4510** |

> [!NOTE]
> *v12's extremely low OOF (0.27) was likely due to job-level leakage from using standard `KFold`. `v16` uses `StratifiedGroupKFold`, which provides a much more realistic (but pessimistic) local estimate.

## 🚀 Next Steps
- **Contractor Win-Rate Features**: Re-integrate the `con_win_rate` and `con_rank_avg` features from `v12` into the `GroupKFold` pipeline.
- **Pseudo-Labeling**: v12 mentioned `submission_v6_elite.csv`—investigating its role in reaching the 0.39 score.
- **Hyperparameter Optimization**: Refining XGBoost and LightGBM parameters for the fusion features.

render_diffs(file:///home/kizabgd/Desktop/Istrazivanje/construction_bidding/bidding_v16_trinity_fusion.py)
