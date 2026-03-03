# 🏀 March Machine Learning Mania 2026 — Grandmaster Plan

**Goal**: Top 10 on the leaderboard. Metric: Brier Score (lower = better).  
**Deadline**: March 19, 2026 | **Current participants**: ~155

---

## Competition Overview

Predict the probability that `Team1` (lower TeamID) beats `Team2` for **every possible matchup** among all 363 Men's and Women's tournament teams. The tournament hasn't started yet — Stage 1 uses historical data for validation.

---

## Strategy: Trinity Ensemble (3 Shots)

### Shot 1 — Elo + Seed Baseline (Fast, Solid)
- Build an Elo rating system using all regular season + tournament games (2003–2025)
- Seed difference as primary feature  
- Elo difference as secondary feature
- Logistic regression to calibrate probabilities
- Expected Brier Score: ~0.220

### Shot 2 — ML Feature Engineering (Efficiency Metrics)
- All Shot 1 features PLUS:
  - **Offensive Rating**: Points scored per 100 possessions
  - **Defensive Rating**: Points allowed per 100 possessions
  - **Net Rating** = ORtg - DRtg
  - **Pace**: Possessions per 40 minutes
  - **eFG%**: Effective Field Goal Percentage
  - **TOV%**: Turnover rate
  - **OREB%**: Offensive rebound rate
  - **Late season weighting** (last 20 games weighted 2x)
  - **Massey Ordinals**: Aggregate of 30+ ranking systems
  - **Conference strength features**
  - **Head-to-head history**
- XGBoost + LightGBM + CatBoost ensemble
- Cross-validated on past tournament years (2015–2025)
- Expected Brier Score: ~0.200

### Shot 3 — Hyper-tuned + Calibration
- All Shot 2 features PLUS:
  - **Tempo-free stats** (efficiency per possession)
  - **SOS** (Strength of Schedule)
  - **Bayesian Elo** with home/away adjustments  
  - **KenPom-style metrics** computed from raw data
  - **Isotonic regression calibration** on prediction layer
  - **Men + Women unified model** with gender flag
  - **Optuna hyperparameter tuning**
  - Stochastic ensemble blending
- Expected Brier Score: ~0.185

---

## Proposed Changes

### Core Pipeline

#### [NEW] march_mania_shot1.py — Elo Baseline
- Compute Elo ratings for all teams per season
- Extract seed-based features from MNCAATourneySeeds
- Generate predictions for all pairs in SampleSubmissionStage1
- Submit as Shot 1

#### [NEW] march_mania_shot2.py — ML Ensemble
- Compute 4-factor stats (OffRtg, DefRtg, Pace, eFG%, etc.)
- Integrate Massey ordinal rankings
- Build XGBoost + LightGBM ensemble trained on historical tourney data
- Submit as Shot 2

#### [NEW] march_mania_shot3.py — Grandmaster Final
- KenPom-style metrics + isotonic calibration + Optuna tuning
- Submit as Shot 3

---

## Verification Plan

### CV Validation
- Leave-one-year-out cross validation on 2015–2025 tournament results
- Report CV Brier Score for each shot

### Kaggle Submission
- `kaggle competitions submit -c march-machine-learning-mania-2026 -f submission.csv -m "Shot N"`
- Compare public LB scores across 3 submissions
- Best submission = Shot 3 (expected)
