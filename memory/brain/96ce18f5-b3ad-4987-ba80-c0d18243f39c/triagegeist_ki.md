# Knowledge Item: TriageGeist Competition Analysis

Detailed breakdown of the **TriageGeist** clinical AI competition.

## 1. Overview & Problem Statement
- **Sponsor**: Laitinen-Fredriksson Foundation (Finland).
- **Domain**: Emergency Department (ED) Triage.
- **Problem**: Extreme cognitive load on clinicians leads to triage errors.
- **Objective**: Assist clinicians by predicting **triage acuity** (ESI levels 1–5) and identifying risk factors or systemic biases.

## 2. Evaluation: The Rubric (100 Points)
This is **NOT** a leaderboard-only competition. Solutions are judged by humans using a rubric:
- **Clinical Relevance (25 pts)**: Alignment with ED workflow and medical reality.
- **Technical Quality (30 pts)**: Reproducibility, code quality, and methodology.
- **Documentation (20 pts)**: Clarity of the notebook and the final writeup (max 2,000 words).
- **Insights (15 pts)**: Discovery of meaningful clinical patterns (e.g., bias detection).
- **Novelty (10 pts)**: Original approaches to feature engineering or modeling.

## 3. Data Ecosystem
| File | Features | Key Signal |
| :--- | :--- | :--- |
| `train.csv` | Age, Sex, Arrival Mode, Vitals (BP, HR, RR, Temp, SpO2) | Patient baseline state & stability. |
| `chief_complaints.csv` | **Free-text narratives** from triage nurses | NLP requirements (BERT/Biowordvec). |
| `patient_history.csv` | 26 Binary flags for chronic conditions (DM, HTN, etc.) | Long-term risk context. |
| **Target Variable** | `triage_acuity` | Ordinal scale 1 (Urgent) to 5 (Non-urgent). |

## 4. Required Deliverables
1. **Public Kaggle Notebook**: Must contain the end-to-end pipeline.
2. **Project Writeup**: Max 2,000 words explaining the methodology and clinical value.
3. **`submission.csv`**: Predictions for the test set.

## 5. Strategic Connection (Heart Disease Elite)
- **Vitals Processing**: The `robust_scale` and `kbins` logic from the Heart Disease project are directly applicable to the vitals in `train.csv`.
- **Ensembling**: CatBoost/LightGBM blends will work well for the tabular parts.
- **New Requirement**: Need to integrate **Natural Language Processing (NLP)** for the `chief_complaints.csv` and merge `patient_history.csv` using `patient_id`.

> [!IMPORTANT]
> Since evaluation is rubric-based, **Explainable AI (XAI)** (SHAP, LIME) and clear visualizations are just as important as the AUC/F1 score.
