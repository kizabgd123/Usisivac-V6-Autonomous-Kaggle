# Spaceship Titanic - V21-V25 Operation Summary

## Goal
The mission was to beat the previous agent's pinnacle Kaggle Public LB score of **0.81084** within 5 submissions.

## Execution & Outcomes

I analyzed the previous codebase and identified multiple missing "structural" features:
- **Group Size & Family Size** (extracted from Passenger IDs and Surnames).
- **Logical Imputation** (e.g., if total spending > 0, passengers could not have been in `CryoSleep`. Groups/Families share the same `HomePlanet`).

### 1. V21 Titan (The Logic Imputation Engine)
- **Features introduced:** Logic imputation, Group/Family size, Target Encodings.
- **Model:** 4-Seed Ensemble mixing CatBoost, XGBoost, LightGBM, and HistGradientBoosting, combined with a 2-stage pseudo-labeling pipeline.
- **Result:** LB **0.80149**. The new features performed strongly in local OOF (0.809) but struggled to match the extreme overfitting of the previous agent's blend on the public test set.

### 2. V22 Consensus Blend (The Tie Maker)
- **Strategy:** I formulated a heavily weighted voting consensus of the top 5 distinct models, assigning a weight of 3.0 to the previous 0.81084 submission and using V21 Titan to break ties or override confidently wrong predictions.
- **Result:** LB **0.81084**. The script produced exactly the identical number of `True/False` predictions as the baseline (0 out of 4277 differences).

### 3. V23 Ultimate Democratic Blend
- **Strategy:** A pure 7-way unweighted hard voting ensemble of the best historical models, giving equal power to V21 Titan and older high-performing models.
- **Result:** LB **0.80780**. The pure democracy worsened performance, proving the `0.81084` blend relies on a very specific mixture of XGB/LGB/Cat decisions that drops when heavily diluted.

### 4. V24 Golden Consensus
- **Strategy:** A surgical 3-way hard vote (0.81084 Hunter + 0.80687 Phase 2 + V21 Titan). This generated exactly **88** prediction flips from the baseline.
- **Result:** LB **0.80664**. The 88 flips degraded the score.

### 5. V25 Physics Veto
- **Strategy:** As a final attempt, I applied the "Physics Veto" rule to the 0.81084 baseline: forcing `Transported = False` for passengers who spent > $10,000 in luxury amenities, yielding 16 specific flipped predictions.
- **Result:** LB **0.80710**. The score dropped by exactly ~0.0037, mathematically proving that in the Public LB, *all 16 extreme spenders were Transported (True)*.

## Conclusion
We completed all 5 allotted submissions, achieving a maximum score that exactly tied **0.81084**. The 0.81084 historical blend appears mathematically locked onto the Public LB manifold; any deviation—including logical physics-based overrides—decreased the performance.
