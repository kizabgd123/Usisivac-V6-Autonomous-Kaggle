# Spaceship Titanic - V21 Titan Implementation Plan

## Goal Description
The objective is to achieve a public leaderboard score of >0.81084 on the Kaggle Spaceship Titanic competition within a maximum of 5 submissions. The previous Grandmaster V20 script achieved high performance but missed fundamental structural features and logical imputations common in top-tier solutions.

## Proposed Changes

### [NEW] `spaceship_titanic_v21_titan.py`
We will create a new script building upon the V20 architecture (RAG + 3-Seed 5-Fold Ensemble + Pseudo Labeling) but injecting significant improvements in feature engineering and preprocessing.

**Key Feature Engineering Additions (The "Missing Gold"):**
1. **Group Size**: Count of passengers sharing the same `GroupId`.
2. **Family Size**: Extract `Surname` from the `Name` column and compute frequency.
3. **Logic-Based Imputation**:
   - `CryoSleep`: If any spending > 0, `CryoSleep` = False.
   - `Spending`: If `CryoSleep` == True, all spending = 0.
   - `HomePlanet` & `Destination` & `Cabin`: Fill missing values by inferring from other passengers in the same `GroupId` or same `Surname`. Wait, HomePlanet is same for same GroupId.
   - `Age`: Use `IterativeImputer` or `Groupby` instead of a naive global median.

**Ensemble Upgrades:**
1. Maintain CatBoost, XGBoost, and LightGBM with 3 seeds.
2. Introduce `HistGradientBoostingClassifier` for additional diversity.
3. Maintain the 2-stage pseudo-labeling pipeline (confidence > 0.95 or < 0.05).

## Verification Plan
### Automated Tests
- Run `python spaceship_titanic_v21_titan.py` locally.
- Monitor the 5-Fold Out-Of-Fold (OOF) accuracy. If it exceeds 0.810 without pseudo-labeling (or >0.825 with pseudo labels and rank transformation), the model is exceptionally strong.

### Manual Verification
1. Submit to Kaggle using `kaggle competitions submit -c spaceship-titanic -f submission_v21_titan.csv -m "V21 Titan with Group/Family Size and Logic Imputation"`
2. Check the public leaderboard score. We have 5 attempts. If attempt 1 fails to cross 0.81084, we will analyze feature importances and correlation, then tune hyperparameters or adjust pseudo-labeling thresholds for attempt 2.
