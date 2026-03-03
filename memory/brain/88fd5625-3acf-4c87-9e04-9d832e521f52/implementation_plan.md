# implementation_plan.md

# Zoki Reset Enrichment & Final Production Training

This plan outlines the integration of "Zoki Reset saveti" text flags, score updates, and the final production-scale model training for the TriageGeist competition.

## Proposed Changes

### [Text & Feature Engineering]

#### [MODIFY] [text_features.py](file:///home/kizabgd/Desktop/Istrazivanje/alcohol_triage_v2/src/text_features.py)
- Implement `extract_crisis_mitigation_flags` to detect specific keywords from "Zoki Reset" (e.g., "hladan tuš", "brza šetnja", "limun").
- Binary flags: `mild_action` (tuš, limun), `moderate_action` (šetnja).

#### [MODIFY] [feature_engineering.py](file:///home/kizabgd/Desktop/Istrazivanje/alcohol_triage_v2/src/feature_engineering.py)
- Update `calculate_addiction_crisis_score` to incorporate `mild_action` flag (+1 for lower risk/mitigation effort).

### [Pipeline & Reporting]

#### [MODIFY] [alcohol_triage_pipeline.py](file:///home/kizabgd/Desktop/Istrazivanje/alcohol_triage_v2/alcohol_triage_pipeline.py)
- Ensure the pipeline uses the updated text metadata.
- Trigger full training on 110k rows.

#### [NEW] [report.ipynb](file:///home/kizabgd/Desktop/Istrazivanje/alcohol_triage_v2/notebooks/report.ipynb)
- Comprehensive evaluation: Confusion Matrix, OOF metrics (Macro-F1, QWK).
- Top 10 SHAP features with clinical justifications.
- Example inference for specific "tremor" query.

## Verification Plan

### Automated Tests
- Run `python3 alcohol_triage_pipeline.py` and verify graduation from preprocessing.
- Verify Kaggle submission via CLI.

### Manual Verification
- Review SHAP force plot in the generated notebook.
