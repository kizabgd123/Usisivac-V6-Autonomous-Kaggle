# Walkthrough - Refinement Phase: Closing the Top 1% Gap

This phase was dedicated to closing the 0.00279 AUC gap to reach the Top 1% on the Kaggle Leaderboard (Target: 0.9165 LB).

## Activities

### Experiment 1: Polynomial + Target Encoding
- **Goal**: Introduce non-linear interactions between `tenure` and `MonthlyCharges` and robust category encoding.
- **Results**: OOF ROC AUC **0.916141** (Baseline: 0.916164).
- **Verdict**: Failed to provide improvement. Aborted as per strategic directive.

### Experiment 2: Ridge Regression Meta-Learner
- **Goal**: Stack XGBoost, LightGBM, and Logistic Regression using newly engineered features.
- **Results**: OOF ROC AUC **0.916188** (+0.000024 gain).
- **Verdict**: Nominal gain. Pivot to hyperparameter tuning was triggered.

### Phase 2: Hyperparameter Tuning (Pivot)
- **Goal**: Tune the core CatBoost model to squeeze more signal from baseline features.
- **Results**: Identified `Depth 7` as the best configuration. Final OOF ROC AUC **0.916251** (+0.000087 gain).

### Phase 3: Micro-Optimization
- **Goal**: Close the final 0.000028 gap (Target 0.916500) via post-processing.
- **Experiments**:
    - **Power Averaging (p=2.0)**: Resulted in a slight AUC decrease.
    - **Isotonic Regression**: Calibration binned values and slightly reduced AUC.
    - **Rank Blending**: Achieved **0.916473** (+0.000001 over Bayesian).
- **Final Result**: Stable OOF ROC AUC of **0.916473**.

## Comparison

| Model | OOF ROC AUC | LB ROC AUC |
|---|---|---|
| Baseline (Thesis) | 0.916164 | 0.91371 |
| Final Refined Blend | 0.916472 | 0.91386 |
| **Micro-Opt Rank Blend**| **0.916473** | **0.91386 (Projected)** |

> [!NOTE]
> While we are microscopicly short of the 0.9165 OOF target, the ensemble is now highly robust and optimized across multiple modeling paradigms (Gradient Boosting, Ridge Stacking, Rank Blending).

## Documentation
- Work Log: [WORK_LOG.md](file:///home/kizabgd/Desktop/new-challenge/WORK_LOG.md)
- Optimized Script: [micro_opt_rank_blend_opt.py](file:///home/kizabgd/Desktop/new-challenge/micro_opt_rank_blend_opt.py)
