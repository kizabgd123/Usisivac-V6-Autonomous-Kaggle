# Trinity Protocol Restoration & Finalization

This plan aims to fix the regression in the Construction Bidding competition and complete the Heart Disease submission pipeline.

## Proposed Changes

### [Construction Bidding]

#### [NEW] [bidding_v14_trinity_fix.py](file:///home/kizabgd/Desktop/Istrazivanje/construction_bidding/bidding_v14_trinity_fix.py)
A robust hybrid model based on the successful v12 architecture:
- **Feature Restoration**: Re-integrate item-level "market estimates" from `raw_train.csv` and `raw_test.csv`.
- **Inflation Correction**: Restore the 2018-2025 inflation mapping.
- **Robust Encoding**: Switch from global target encoding to in-fold smoothed encoding to prevent leakage.
- **Ensemble**: CatBoost + LightGBM + XGBoost weighted blend.
- **Calibration**: Use Isotonic Regression for final price adjustment.

### [Heart Disease]

#### [RUN] [heart_v6_final_combined.py](file:///home/kizabgd/Desktop/Istrazivanje/heart_v6_final_combined.py)
Execute the final production script to generate the submission for current S6E2 state.

---

## Verification Plan

### Automated Tests
- **Bidding v14 Dry Run**: Run `bidding_v14_trinity_fix.py` with 3 folds to verify OOF RMSLE matches v12 range (~0.27).
- **Heart Disease Verify**: Check if `submission_v6_pseudo_uci.csv` is generated with 630k+ predictions.

### Manual Verification
- Verify the public LB score of Bidding v14 by submitting to Kaggle.
