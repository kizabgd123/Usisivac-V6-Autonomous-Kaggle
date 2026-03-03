# Implementation Plan: Score Improvement — v8 Pipeline

## Forensic Analysis

| Submission | LB Score | Key Technique |
|---|---|---|
| v7 (our clean baseline) | 0.95379 | CatBoost+LGB, 3-fold HPO on 50k sample |
| `submission_colab_0.95573` | **0.95387** | CatBoost+LGB, 5-fold HPO on full dataset + pseudo-label |
| `submission_improved_0.95574` | **0.95386** | Same architecture, different seed |
| v10.13 Grandmaster (Kaggle kernel) | ~0.95340 | XGB+LGB+CAT+HistGB+MLP+Stacking — ran on Kaggle CPU, limited iters |

**Root cause of v7 sub-par score:**
1. HPO used only 3-fold on 50k sample → weaker parameter discovery
2. Only 2 CatBoost seeds (42, 123) — more seeds = better averaging
3. No XGBoost in ensemble → correlation reduction opportunity missed
4. No pseudo-labeling at all (removed to fix leakage, but safe PL can help)

**Target:** LB ≥ 0.95410 (OOF ≥ 0.957)

## Proposed Changes: v8 Pipeline

### Strategy
Upgrade `instrumented_pipeline.py` with:
1. **XGBoost added** to ensemble (3-model blend: CatBoost + LGB + XGB)
2. **5-fold HPO on full dataset** (3-fold was too weak)
3. **3 CatBoost seeds** (42, 123, 456) instead of 2
4. **Safe pseudo-labeling** with 10% holdout gating (only accept if holdout AUC improves)
5. **Rank-averaging blend** instead of linear blend (more robust)

> [!IMPORTANT]
> **Safe Pseudo-Labeling**: Pseudo labels are selected ONLY from test set predictions. The holdout set (10%, stratified split BEFORE any training) acts as a gate — PL is only accepted if `holdout_auc_phase2 > holdout_auc_phase1`. This prevents leakage.

---

### Files to Modify

#### [MODIFY] [instrumented_pipeline.py](file:///home/kizabgd/Desktop/Istrazivanje/instrumented_pipeline.py)

**Section 1 — New imports:**
```python
import xgboost as xgb
from sklearn.model_selection import train_test_split
from scipy.stats import rankdata
```

**Section 2 — Add 10% holdout split before training:**
```python
from sklearn.model_selection import train_test_split
X_main, X_hold, y_main, y_hold = train_test_split(
    X_tr_full, y, test_size=0.10, stratify=y, random_state=42)
```

**Section 3 — Expand HPO:**
- Use full dataset (not 50k sample)
- Keep 3-fold (for speed), but on ALL data
- Add XGBoost objective function to HPO

**Section 4 — Production training:**
- CatBoost: 3 seeds × 5 folds  
- LightGBM: 2 seeds × 5 folds  
- XGBoost: 2 seeds × 5 folds  

**Section 5 — Safe pseudo-labeling:**
```python
# Phase 2: Safe PL (only if holdout AUC improves)
blend_pred_phase1 = alpha*pred_cat + (1-alpha)*pred_lgb + (1-alpha)*pred_xgb
holdout_auc_phase1 = roc_auc_score(y_hold, alpha*oof_cat_hold + ...)
# ... retrain with pseudo-labels ...
# Accept only if holdout_auc_phase2 > holdout_auc_phase1
```

**Section 6 — Rank-averaging blend:**
```python
from scipy.stats import rankdata
# Rank-normalize each model's predictions, then average
```

## Verification Plan

### Automated Tests
- Run `python3 instrumented_pipeline.py`
- Expected OOF ≥ 0.957
- Holdout AUC gap vs OOF < 0.003 (confirms no leakage)

### Manual Verification
- Submit to Kaggle
- Expected LB ≥ 0.95410
- Expected gap OOF-LB < 0.003
