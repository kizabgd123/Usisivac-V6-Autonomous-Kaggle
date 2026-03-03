# KillShot v3.3 — Closing the Gap to 0.960+

## Problem
v3.2 achieved OOF AUC 0.955338. Top solutions reach 0.964. The gap analysis identified 10 missing techniques, primarily **Target Encoding** and **9 missing top-ranked features**.

## Proposed Changes

### Feature Engineering

#### [NEW] [heart_top5_v3_3.py](file:///home/kizabgd/Desktop/Istrazivanje/heart_disease/heart_top5_v3_3.py)

Based on v3.2, adding:

**1. Target Encoding (CV-safe):**
```python
for col in ['Chest pain type', 'Thallium', 'Slope of ST', 'EKG results']:
    # Fold-wise target encoding to prevent leakage
    target_enc = train_fold.groupby(col)['Heart Disease'].mean()
    val_fold[f'{col}_TE'] = val_fold[col].map(target_enc)
```

**2. Top Missing Interactions:**
- `Thallium_ChestPain` = Thallium × Chest pain type
- `Health_score` = (Max HR / (220 - Age)) × (1 - Exercise angina)
- `Sex_ChestPain` = Sex × Chest pain type
- `Age_Sex` = Age × Sex
- `Vessels_Thallium` = Number of vessels × Thallium
- `HR_Age_ratio` = Max HR / Age
- `ST_HR_ratio` = ST depression / (Max HR + 1)
- `Vessels_Age_ratio` = Number of vessels / (Age + 1)
- `CV_risk_score` = Age + BP/10 + Cholesterol/50 + FBS × 10
- `Multiple_risks` = (Exercise angina + FBS + (Slope>1)) ≥ 2

**3. OHE for Pseudo-Categoricals:**
```python
ohe_cols = ['Chest pain type', 'EKG results', 'Slope of ST', 'Thallium']
train = pd.get_dummies(train, columns=ohe_cols, drop_first=True)
```

**4. Multi-Seed (3 seeds):** `SEEDS = [42, 123, 777]`

## Verification Plan

### Automated Tests
- Compare OOF AUC v3.3 vs v3.2 (0.955338 baseline)
- Adversarial validation (expect ~0.50)
- Feature importance ranking to confirm new features contribute
