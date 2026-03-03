# Implementation Plan: Bidding# V12 Overdrive (Revised) - Public LB Focus

> [!WARNING]
> **LEAKAGE DETECTED**: The previous iteration of V12 had a data leak in the Bayesian priors. This led to an artificially low OOF score (~0.27). The plan is now revised to ensure strict validation.

Objective: Achieve Public LB < 0.30 by maximizing model capacity and using full-history features.

## Proposed Changes

### 3. Model Training: 10-Fold K-Fold
- Switch from temporal split (2024) to **10-Fold Shuffled K-Fold**.
- This allows the model to learn patterns from the most recent 2024 data while still having enough volume to avoid overfitting to specific months.

### 4. Recursive Pseudo-Labeling
- Use a blend of V6 (0.398) and V11 (0.418) to generate targets for the test set.
- Filter only the top 500 test jobs with the lowest variance between V6 and V11.
- Add these back into the training pool.

## Verification Plan
1. **Local CV**: target 10-Fold OOF RMSE < 0.25 (Log space).
2. **Leaderboard**: Submit and verify Public LB jump.
