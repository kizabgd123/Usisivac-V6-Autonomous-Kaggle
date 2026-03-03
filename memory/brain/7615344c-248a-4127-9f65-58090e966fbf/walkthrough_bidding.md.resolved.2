# Walkthrough: Bidding V10 Zenith Submission

## Overview
V10 "Zenith" was designed to recover from the performance collapse of V7-V9 (which dropped to 0.68 LB). By reverting to robust median-based price estimation while adding contractor strategy features, we achieved a strong Public LB score.

## Submission Results

| Version | Description | Public LB | Status |
| :--- | :--- | :--- | :--- |
| **V10 Zenith** | **Ridge Stacking + Contractor DNA + Robust Median** | **0.4172** | **Top Score (Post-V6)** |
| V9 Apex | Absolute Target + Stacking | 0.6680 | Partial Success |
| V8 Sovereign | Robust Median + DNA (Initial) | 0.6823 | Failure |
| V7 Piercer | Direct Price Prediction (LGBM) | 0.6430 | Failure |
| **V6 Elite** | **Simple Median + K-Fold Ensemble** | **0.3980** | **Baseline to beat** |

## Performance Analysis
V10 achieved **0.4172**, which is a significant recovery from the mid-pipeline collapse.

### Why V10 succeeded where V7-V9 failed:
1.  **Robust Medians**: V7's attempt to use LGBM for every single pay-item price was too noisy. V10 returned to median-based "market price" estimates, which are much more stable.
2.  **Absolute Reconstruction**: Predicting the bid as a sum of estimated parts (then refining the total) proved superior to predicting a raw total from high-level features.

### Why V6 still holds a slight edge (0.019 diff):
1.  **Leakage vs. Robustness**: V6 used a random 5-fold CV which might have some data leakage (as identified in previous logs). V10 uses a strict temporal split (2024), making it more "honest" but potentially missing some local patterns in the Public LB.
2.  **Price Reference Scope**: V6 used 100% of the training data to calculate median prices. V10 used only pre-2024 data. If 2024 prices are closer to the 2025 test set, V6 has a manual advantage.

## Next Steps
We have successfully stabilized the pipeline. The next move is to fine-tune the "Contractor Multiplier" approach to shave off the final 0.02 to beat V6 and approach the Top 1.

![Leaderboard Status](file:///home/kizabgd/Desktop/Istrazivanje/construction_bidding/run_log.txt)
