# Trinity Protocol Evolution Task List

## Documentation & Protocol Stabilization
- [x] Initialize `GEMINI.md` with Project Constitution (Trinity Protocol Q&A)
- [x] Align system behavior with `/PRODUCT_GUARDIAN_PROTOCOL`

## Unification of Launch Mechanism
- [x] Research existing entry points and script sprawl
- [x] Create universal `Makefile` for standard commands
- [x] Implement `trinity` CLI tool (Phase 1: Entry Point Abstraction)
- [x] Design and implement `manifest.json` schema for declarative execution
- [x] Implement `Legacy Integration Protocol` (Auto-generation of manifests/makefiles)

## Process Hardening (ProcessGuard)
- [x] Design `ProcessGuard` as an evolution of `JudgeGuard`
- [x] Implement correlation checking and performance monitoring
- [x] Move hardcoded thresholds to domain-specific config files
- [x] Integrate ProcessGuard into more pipeline stages

## Memory & Reliability
- [x] Optimize memory hashing strategy (Implemented milestone-based hashing)
- [x] Implement `ToolRegistry` for modular feature engineering (Completed scaffold and registry)
- [x] Add metric-based "Fail-Gate" for low-performance/highly-correlated models
- [x] Add metric-based "Fail-Gate" for low-performance/highly-correlated models

## [ACTIVE] Constitutional Hardening v2.0
- [x] Update `GEMINI.md` with Meta Command & Internal Consistency Laws
- [x] Implement JSON SSOT in `trinity.py`
- [x] Create `error_handler.py` for structured feedback
- [x] Refactor `MemoryIntegrity` for metadata/raw separation
- [x] Implement Parquet-based logging for microactions

## [IN-PROGRESS] Debugging & Revenue-Driven Optimization
- [x] Fix syntax errors in `instrumented_pipeline.py`
- [x] Resolve `JudgeGuard` log requirements
- [x] Standardize SSOT integration via `config_manager.py` (Verified via `trinity.py info`)
- [x] Optimize training pipeline for ROI (CatBoost Production Retrain: 2713 iterations, AUC ~0.96964)
- [x] Verify end-to-end execution via `trinity.py`
- [x] Integrate with Kaggle CLI (Pending competition access validation)

## [IN-PROGRESS] Overfit Recovery & Leakage Elimination
- [x] Forensic audit of `instrumented_pipeline.py` (Identified Pseudo-Labeling Leakage)
- [x] Draft recovery plan (Remove pseudo-labeling, conservative retrain)
- [x] Implement removal of leakage loop (Fixed `NameError` in `instrumented_pipeline.py`)
- [x] Re-verify clean OOF vs LB alignment (Clean OOF Blend AUC: 0.95563 — CatBoost: 0.95561, LightGBM: 0.95540)
- [x] Generate clean submission file (`submission_v7_clean_baseline_0.95563.csv`)
- [x] Submit to Kaggle and verify LB alignment (LB: 0.95379, Gap: 0.0018 ✅ — vs. previous 0.0175 gap)






## Modularization of Elitist Techniques
- [x] Scaffold Feature Engineering Tool Registry
- [x] Migrate Tabular RAG to independent plug-and-play module
- [x] Verify ToolRegistry modular execution (Verified via `verify_components.py`)

## Memory Hardening
- [x] Implement milestone-based integrity hashing
- [x] Integrate hashing into Trinity lifecycle
- [x] Verify MemoryIntegrity mechanism

## [TODO] Elite Strategy Implementation v9 (Post-v8)
- [ ] Integrate Original UCI Dataset (`redwankarimsony/heart-disease-data`) into training data to dilute GAN noise.
- [ ] Implement Periodic Embeddings for `Age` and `MaxHR` (Sine/Cosine transformations).
- [ ] Implement OOF Target Encoding for `ChestPainType`, `Thallium`, and `EKGresults`.
- [ ] Explore Logistic Regression Stacking meta-model instead of simple rank averaging.
- [ ] Apply Product Guardian Protocol: ensure strict separation of training-only UCI data.

## ML Metrics Research
- [x] Compile guide on tracking ML metrics (`ml_metrics_tracking_guide.md`)
