# Walkthrough: TriageGeist + Heart Disease Deep Analysis

## Summary of Work

I've done a complete multi-source analysis using Kaggle CLI, browser, and direct code inspection.

## 1. TriageGeist Competition — Key Findings

> [!IMPORTANT]
> **TriageGeist is a Hackathon, NOT a standard Kaggle competition.**
> The `NOTE.md` file explicitly states: _"This is a Hackathon with no provided dataset. Please refer to kaggle.com/competitions/triagegeist/data for data inspiration."_

| Property | Value |
| :--- | :--- |
| URL | https://www.kaggle.com/competitions/triagegeist/ |
| Prize | $10,000 USD |
| Deadline | 2026-04-21 |
| Target | `triage_acuity` (ESI 1–5, ordinal) |
| Test size | 20,000 patients |
| Data | Bring-your-own (inspiration files provided) |

### The Data Files (Inspiration)

| File | Description |
| :--- | :--- |
| `train.csv` | Demographics + vitals (BP, HR, Temp, SpO2, GCS, Pain) |
| `chief_complaints.csv` | **Free-text triage narratives** → BioBERT/TF-IDF |
| `patient_history.csv` | 26 chronic condition binary flags |
| `test.csv` | Same as train, no target |

### Evaluation: Rubric (100 pts)
- **Technical Quality** — 30 pts
- **Clinical Relevance** — 25 pts
- **Documentation** — 20 pts
- **Insights & Novelty** — 25 pts

## 2. OCR Transformation

I developed a Python-based OCR pipeline to convert your scanned PDF into a searchable text format.

- **System**: Tesseract OCR engine + `pdf2image` (300 DPI).
- **Fixes Applied**: 
  - Manually downloaded the Tesseract `srp` (Serbian Cyrillic) language data to properly extract the Cyrillic text.
  - Implemented automatic image rotation using Tesseract OSD (Orientation and Script Detection) because the scanned pages were sideways (90 degrees rotated).
- **Result**: Successfully processed and accurately extracted the Cyrillic text from all 15 pages of "Stavovi o alkoholizmu".
- **Output**: [scan_20260224_175019.txt](file:///home/kizabgd/Desktop/Istrazivanje/scans/scan_20260224_175019.txt)

![First page preview](/home/kizabgd/.gemini/antigravity/brain/96ce18f5-b3ad-4987-ba80-c0d18243f39c/page1_preview-01.jpg)

## 3. Heart Disease v10.14 SOTA — Architecture


Your best-performing notebook uses a **Two-Phase 60-model stacking** architecture:

```
Phase 1: XGB × 3 seeds × 5 folds
         LGB × 3 seeds × 5 folds
         CatBoost × 3 seeds × 5 folds (Pool + native cats)
         MLP × 3 seeds × 5 folds (Periodic Embeddings!)
         → Platt Calibration
         → 10-fold LogReg meta-stacker

Phase 2: Conditional PL (only if Holdout < 0.9542)
         → Weight 0.30, consensus ≥ 8 of 12 models required
```

### Top 3 Innovations in v10.14
1. **Flipped Label Scrubbing** — Removes `Presence` labels that are physiologically impossible
2. **Gaussian Periodic Embeddings** — MLP uses sin/cos projections of numeric features
3. **Rank-based Ensembling** — Normalized ranks instead of raw probs = robust to scale

## 3. Artifacts Created

| File | Purpose |
| :--- | :--- |
| [AGENT_KNOWLEDGE_BASE.md](file:///home/kizabgd/.gemini/antigravity/brain/96ce18f5-b3ad-4987-ba80-c0d18243f39c/AGENT_KNOWLEDGE_BASE.md) | **Master reference** — all agents should read this first |
| [triagegeist_ki.md](file:///home/kizabgd/.gemini/antigravity/brain/96ce18f5-b3ad-4987-ba80-c0d18243f39c/triagegeist_ki.md) | TriageGeist detailed analysis |
| [heart_disease_elite_ki.md](file:///home/kizabgd/.gemini/antigravity/brain/96ce18f5-b3ad-4987-ba80-c0d18243f39c/heart_disease_elite_ki.md) | Heart Disease FE + pseudo-labeling |
| [pdf_to_text.py](file:///home/kizabgd/Desktop/Istrazivanje/scripts/pdf_to_text.py) | Automation script for OCR extraction. |
