# Spaceship Titanic - Phase 4: Calibration & Selective Integration

Ova faza se fokusira na povratak osnovama, dekompoziciju greške i uvođenje nelinearnih grupnih signala (Survival Rate).

## Proposed Changes

### [Component: Domain-Driven Group Logic]

#### [NEW] [spaceship_titanic_calibration.py](file:///home/kizabgd/Desktop/kaggle-arena/scripts/spaceship_titanic_calibration.py)
Implementacija kalibrisanog cevovoda:
- **Family & Ticket Survival Rate:**
    - Ekstrakcija prezimena iz `Name`.
    - Grupisanje po `GroupId` i `CabinNum`.
    - Izračunavanje stope preživljavanja unutar ovih grupa (fold-safe) uz smoothing.
- **Target Encoding De-biasing:**
    - Stroga primena $k-1$ fold fitting-a.

### [Component: Selective Integration Ensemble]

#### [STRATEGY] Selective Voting (Majority Vote)
- Zamena Lasso meta-modela sa selektivnim ansamblom.
- GBDT modeli ostaju primarni pokretači, SVM/MLP služe za korekciju nelinearnih splitova.
- Implementacija "Tie-break" logike zasnovane na modelu sa najboljim OOF rezultatom.

#### [REFINEMENT] Hyperparameter Tuning
- Re-tuning `max_depth` i `min_child_weight` za XGB/LGBM radi kontrole overfitting-a.

## Verification Plan

### Automated Tests
- `python3 scripts/judge_guard.py --action "Training Calibration"`
- Provera: Korelacija predikcija (SVM vs GBDT) < 0.85.
- Target Accuracy: **LB > 0.80**.

### Manual Verification
- Vizuelizacija Feature Importance (Explainable AI) za `Survival_Rate` karakteristike.
- Finalna submisija.
