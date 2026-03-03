# Kaggle Bidding Recovery Plan (v26)

## Problem
- `v25` OOF/LB is significantly worse than `v23`.
- Root cause: Unstable `bid_ratio` engineering and overly restrictive `GroupKFold`.

## Proposed Changes
### `bidding_v26_stabilized_synthesis.py`
- **CV Strategy**: Revert to 10-Fold Shuffled `KFold` (matching `v23` breakthrough).
- **Features**:
    - Simplifed `market_est` (Log-space, no inflation).
    - Seasonal features (`is_winter`).
    - Remove `bid_ratio` and `con_bid_variance`.
- **Ensemble**: Maintain 5-way hybrid for diversity.

## Verification
- Target OOF RMSLE: < 0.30.
- Target LB Score: < 0.40.
