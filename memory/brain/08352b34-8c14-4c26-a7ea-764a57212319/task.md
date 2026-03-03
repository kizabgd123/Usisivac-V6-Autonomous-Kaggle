# Task Checklist

- [x] Analyze existing code and data for S6E2
- [x] Implement Elite Features (RPP, Thal-Pain Interact)
- [x] Implement Phase 1: Cleanlab Noise Detection (OOF Dirty Model)
- [x] Purge Noisy Features (Duke Score removed)
- [x] **[FIX]** Standardize UCI Mapping (Strict enforcement)
- [x] **[FIX]** Implement Consistent Isotonic Calibration (OOF & Test)
- [x] Implement Phase 2: Calibrated XGB + LGBM Ensemble
- [x] Implement Phase 3: Auto-Selection (Simplex vs Stacking)
- [x] Generate Final Submission (`submission_final_exec.csv`)
- [x] **[OPTIMIZE]** Parallelize SOTA Pipeline (`heart_pipeline_v10_14_sota.py`)
- [x] **[UPGRADE]** Integrate Cleanlab Denoising into SOTA Pipeline
- [x] **[VERIFY]** Trinity Killshot Registry Integrity

## Constitutional Audit
- [x] **F2 (Istina)** — Verify factual accuracy τ >= 0.99
- [x] **F7 (Poniznost)** — Verify uncertainty retention [0.03, 0.05]
- [x] **F8 (Genius)** — Internal consistency > 0.80
- [x] **Rule 27** — Memory integrity (parquet + SHA-256)
- [x] **Killshot Readiness** — SSOT hierarchy, ProcessGuard, ToolRegistry
