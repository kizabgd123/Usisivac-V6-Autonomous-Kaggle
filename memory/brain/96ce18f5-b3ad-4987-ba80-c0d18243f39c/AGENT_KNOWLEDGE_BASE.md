# 🚨 PERMANENT KNOWLEDGE BASE — FOR ALL AGENTS
> Last updated: 2026-02-24. Always consult this file before starting any work related to TriageGeist or Heart Disease S6E2.

---

## ════ PART 1: TRIAGEGEIST COMPETITION ════

### 1.1 Competition Identity
- **URL**: https://www.kaggle.com/competitions/triagegeist/
- **Type**: Community Hackathon ($10,000 USD prize)
- **Sponsor**: Laitinen-Fredriksson Foundation (Finland)
- **Deadline**: 2026-04-21 22:00:00 UTC
- **Enrolled**: ✅ Yes (user has entered)
- **Teams so far**: 4

> [!IMPORTANT]
> This is a **Hackathon**, NOT a classic Kaggle leaderboard competition. The NOTE.md file explicitly says:
> `"Welcome! This is a Hackathon with no provided dataset. Please refer to kaggle.com/competitions/triagegeist/data for data inspiration."`
> This means the data should be **sourced by the participant**. The Kaggle data tab provides example/inspiration files only.

### 1.2 Problem Statement
Build an **AI-powered clinical decision support system** to help Emergency Department (ED) clinicians make rapid triage decisions. ED clinicians face extreme cognitive load with incomplete information. Errors in ESI-level assignment lead to delayed care, adverse outcomes, and preventable deaths.

### 1.3 Target Variable
| Column | Description |
| :--- | :--- |
| `patient_id` | Unique ID, format `TG-XXXXXXXX` |
| `triage_acuity` | ESI level 1–5 (1=most urgent, 5=non-urgent). **Ordinal classification task.** |

### 1.4 Data Files (Inspiration/Example Only!)
| File | Size | Content |
| :--- | ---: | :--- |
| `train.csv` | 18.7 MB | Patient demographics + vital signs |
| `test.csv` | 4.4 MB | Same structure as train, no target |
| `chief_complaints.csv` | 6.6 MB | **Free-text nurse triage narratives** — NLP required! |
| `patient_history.csv` | 6.3 MB | 26 binary flags for chronic conditions, medications |
| `sample_submission.csv` | 300 KB | 20,000 test rows, columns: `patient_id`, `triage_acuity` |
| `NOTE.md` | 135 B | States "Hackathon with no provided dataset" |

**Key schema from sample_submission.csv:**
```
patient_id,triage_acuity
TG-FZUFCRZS3,3
TG-SSCOXTYI1,3
```

### 1.5 Evaluation: Rubric-Based (100 Points)
This is **rubric-scored by human judges**, NOT purely leaderboard.

| Category | Points | What it means |
| :--- | ---: | :--- |
| Technical Quality | 30 | Code quality, reproducibility, methodology soundness |
| Clinical Relevance | 25 | Solution must reflect real ED workflow |
| Documentation | 20 | Clear notebook + writeup (max 2,000 words) |
| Insights & Findings | 15 | Clinical patterns, bias detection, explainability |
| Novelty | 10 | Original approach to modeling/FE |

> [!IMPORTANT]
> **Explainable AI (SHAP, LIME) and clinical interpretability are MANDATORY** given the rubric. A black-box model with high accuracy is NOT enough to win.

### 1.6 Required Deliverables
1. **Public Kaggle Notebook** — end-to-end pipeline, must be public at submission time
2. **Project Writeup** — max 2,000 words explaining clinical value
3. **`submission.csv`** — predicted `triage_acuity` for test set

### 1.7 Strategy Notes (from Heart Disease background)
- **Tabular models** (CatBoost + LightGBM) for vitals/demographics in `train.csv`
- **NLP pipeline** (BioBERT, ClinicalBERT, TF-IDF + LG) for `chief_complaints.csv`
- **Patient history merging** via `patient_id` from `patient_history.csv`
- **Multi-modal ensemble**: Blend tabular + text model predictions
- **SHAP values**: Must be generated for clinical interpretability
- **Bias detection**: Analyze performance by sex, age, arrival mode

---

## ════ PART 2: HEART DISEASE S6E2 — WINNING CODE (v10.14 SOTA) ════

### 2.1 Script Identity
- **File**: `heart_pipeline_v10_14_sota.py`  
- **Kaggle Kernel**: `kiza123123/heart-disease-s6e2-v10-14`
- **Version name**: `HEART DISEASE V10.14 — 12 base models`
- **Target**: AUC > ~0.954–0.956 (Holdout)

### 2.2 Architecture: Two-Phase Stacking
```
Phase 1: 4 models × 3 seeds × 5 folds = 60 sub-models
  ├── XGBoost
  ├── LightGBM
  ├── CatBoost (with Pool + native cat features)
  └── MLP (with Gaussian Periodic Embeddings)

↓ Platt Calibration

Meta-stacker: LogisticRegression (C=0.1, 1.0, 5.0) × 10-fold

Phase 2: Conditional Pseudo-Labeling
  └── Only triggered if Phase 1 Holdout AUC < 0.9542
  └── PL weight = 0.30 (low to avoid noise)
  └── Only applied if >= 40 pseudo samples pass consensus filter (≥8/12 models agree)
```

### 2.3 Key Innovations (SOTA-1,2,3)

#### [SOTA-1] Flipped Label Scrubbing
Removes physiologically impossible training labels:
```python
# Presence + Chol=0 + Oldpeak=0 → likely label flip
mask = (df['target']==1) & (df['Cholesterol']==0) & (df['Oldpeak']==0)
# Presence + Age<30 + No Angina + No ST depression → suspect
mask2 = (df['target']==1) & (df['Age']<30) & (df['Oldpeak']==0) & (df['ExerciseAngina']==0)
```

#### [SOTA-2] Gaussian Periodic Embeddings (MLP)
```python
def periodic_embedding(x, n_freqs=8):
    freqs = 2 ** np.arange(n_freqs, dtype=np.float32)
    args = x[:, None] * freqs[None, :] * 2 * np.pi
    return np.concatenate([np.sin(args), np.cos(args)], axis=-1)
```
Applied to: `["Age", "RestingBP", "Cholesterol", "MaxHR", "Oldpeak", "Ischemic", "AgeHR"]`

#### [SOTA-3] Additive Risk Score (no multiplicative noise)
```python
Risk_Score = (Age>55) + (BP>140) + (Chol>240) + ExerciseAngina + Sex
```

### 2.4 Feature Engineering
| Feature | Formula | Clinical meaning |
| :--- | :--- | :--- |
| `Ischemic` | `Oldpeak / (ST_Slope + 0.1)` | Ischemic burden |
| `Young` | `Age < 40` | Atypical presentation flag |
| `BP_Chol` | `BP / (Chol + 1e-6)` | Vascular stress ratio |
| `AgeHR` | `Age × MaxHR` | Combined cardiac load |
| `HRres` | `220 - Age - MaxHR` | Heart rate reserve |
| Binning | AgeBin, BPBin, ChBin | Ordinal risk buckets |
| Freq encoding | For cat cols | Population frequency signal |
| In-fold TE | For cat cols | Leak-free target encoding |
| MI selection | `mutual_info_classif > 0.005` | Remove noise features |

### 2.5 Cholesterol Imputation
```python
# Group median by Sex + ChestPainType
group_med = tr.groupby(["Sex","ChestPainType"])["Cholesterol"].median()
# Zero = missing, NOT zero cholesterol
df["CholMiss"] = (df["Cholesterol"] == 0).astype(int)
```

### 2.6 Model Configs
```python
XGB_CFG  = dict(max_depth=6, min_child_weight=3, colsample_bytree=.8, subsample=.8, lr=0.02)
LGB_CFG  = dict(num_leaves=31, min_child_samples=40, colsample_bytree=.8, subsample=.8, lr=0.02)
CAT_CFG  = dict(depth=6, l2_leaf_reg=5, lr=0.02, iterations=600, early_stopping_rounds=40)
MLP_CFG  = dict(hidden_layer_sizes=(128, 64), max_iter=300, early_stopping=True)
BAG_SEEDS = [42, 123, 2024]
N_FOLDS = 5
HOLDOUT_FRAC = 0.10  # Stable 10% holdout for unbiased eval
```

### 2.7 Execution Flow
1. Load + rename columns (handles both S6E2 and classic Cleveland format)
2. Optionally add external `Heart_disease_statlog.csv` for extra samples + dedup
3. Scrub flipped labels
4. 10% stable holdout split
5. Cholesterol imputation
6. Feature engineering + MI selection
7. Phase 1: 60-model training with Platt calibration
8. Phase 2: Conditional Pseudo-Labeling
9. Rank-based final blend: `meta_rank × α + base_avg_rank × (1-α)`, α tuned on holdout
10. Export `submission_v14_sota_{holdout_auc:.5f}.csv`

### 2.8 Important Code Patterns
- **External data**: Adds `Heart_disease_statlog.csv` if available (deduplicated)
- **CatBoost**: Uses `Pool` objects with explicit `cat_features` by index
- **Rank blending**: `rankdata / n` for normalized rank-based ensemble
- **Platt calibration**: Per-model logistic regression calibration before stacking
- **Conditional PL**: Hard consensus threshold (≥8 of 12 models) for label quality
