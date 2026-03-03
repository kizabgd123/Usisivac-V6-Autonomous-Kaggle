# 🐛 Recovery Plan: Construction Bidding (v17)

## Goal
The goal is to recover from the "TOTALNA KATASTROFA" of `bidding_v16_trinity_fusion.py` (LB 0.4510) and surpass the benchmark set by `bidding_v12_overdrive.py` (LB 0.3981).

## Root Cause Analysis of v16 Failure
1. **Target Leakage**: The `cluster` feature was calculated globally on `total_bid` before the cross-validation loop. This leaked the target variable into the training folds, causing overfitting and invalid OOF scores.
2. **Feature Misalignment (Scrambling)**: The `get_leak_free_market_estimates` in `v16` returned `.values` from a `merge` operation. Because `merge` does not guarantee index preservation, assigning this NumPy array back to the DataFrame completely scrambled the crucial `market_est` feature for the test set, feeding garbage to the models.
3. **Data Truncation**: As noted in `BUG_LOG.md`, `v14` (and potentially aspects of models leading up to `v16`) suffered from truncated training data (9,822 vs 10,621 rows). Though the file was restored, the bad architecture from the corrupted period persisted.

## Proposed Changes

### [NEW] `bidding_v17_recovery.py`
We will create a new script named `bidding_v17_recovery.py` in the `construction_bidding` directory.

**Technical Architecture (The Fix):**
1. **Foundation**: Build strictly upon the proven `bidding_v12_overdrive.py` baseline, ensuring 100% data integrity check at startup (asserting 10,620 rows in `train_summary.csv`).
2. **Leak-Free Market Estimates**: Revert to the safer Pandas-native `merge` assignment from `v12` which guarantees index alignment, completely eliminating the array-scrambling bug.
3. **Target-Leak Removal**: Calculate contractor statistics (like `con_win_rate` and `con_rank_avg`) STRICTLY inside the KFold loop on the `tr_summ` split.
4. **Enhanced Features (from v15, but safe)**: Add the `cnt` (pay items count) and `q_sum` (total quantity) from the raw tables, correctly merged before modeling without using any target features globally.
5. **Ensemble Optimization**: Use an elegant blend of XGBoost, LightGBM, and CatBoost.
6. **Protocol Adherence**: 
   - Integrate `judge_guard.py` hooks via `os.system` or subprocess to automatically log actions in `WORK_LOG.md` (e.g., "Starting v17 Training").

## Verification Plan

### Automated Tests
- Run `python3 bidding_v17_recovery.py` to ensure it executes without errors.
- Verify the standard output includes the exact Data Integrity Check (`Expected 10620`).
- Ensure `submission_v17_recovery.csv` is generated and has exactly 4,776 rows.

### Manual Verification
- The user will submit `submission_v17_recovery.csv` to the Kaggle platform to verify the Public LB score is < 0.3980.
- Check `WORK_LOG.md` to confirm the ANTIGRAVITY-OS protocol was respected (`🟡 Starting Training` \u2192 `✅ Done`).
