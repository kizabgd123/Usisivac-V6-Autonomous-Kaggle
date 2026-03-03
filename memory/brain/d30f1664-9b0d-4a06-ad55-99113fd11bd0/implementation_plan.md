# Fast V3 Elite Pipeline Implementation Plan

Accelerating the Heart Disease prediction pipeline while retaining the architectural improvements from V2.

## Goal
Improve execution speed on the 630k row dataset without compromising the high AUC achieved by the medical feature engineering.

## Proposed Changes

### [Component] Heart Disease Pipeline (V3 - Fast)
#### [NEW] [heart_top5_v3_fast.py](file:///home/kizabgd/Desktop/Istrazivanje/heart_disease/heart_top5_v3_fast.py)
- **Feature Engineering**: Retain all V2 features (Ischemic Burden, Framingham Proxy, Pulse Pressure, etc.).
- **Checkpoint Reuse**: Script will automatically detect and load `lgb.npz` to skip the 50-minute LightGBM training.
- **XGBoost Overhaul**: 
    - Switch `booster` to `gbtree` (standard).
    - Use `tree_method='hist'`.
    - **Speedup**: Remove `DART` which was causing 5h+ stalls.
- **CatBoost Optimization**:
    - Increase `early_stopping_rounds`.
    - Set `thread_count=-1`.
- **Parallelism**: Ensure only ONE instance is running to maximize CPU utilization per fold.

## Verification Plan
### Automated Tests
- Run `heart_top5_v3_fast.py` and verify:
    - LGB Load: Check if it loads the 0.95507 OOF correctly.
    - XGB Speed: Verify fold completion in < 5 minutes instead of > 2 hours.
    - OOF AUC: Monitor to ensure OOF remains > 0.955.

### Manual Verification
- Check `training.log` for consistent AUC reporting across 10 folds for XGB and CatBoost.
