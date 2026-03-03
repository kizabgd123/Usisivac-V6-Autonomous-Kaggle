# Knowledge Base & Model Tracking Implementation Plan

## Goal Description
1. **Knowledge Base Orchestrator**: Sync Notion KB to local SQLite index.
2. **Heart Disease Pipeline**: Track Optuna trials for model tuning in `heart_disease_top3_colab.py`.
3. **Spaceship Titanic Notebook**: Enhance `Untitled-2.ipynb` (or its eventual content) to track Optuna trials, AUC, and AUF (Accuracy/Metrics) using Arize Phoenix.

## Proposed Changes

### Spaceship Titanic Tracking

#### [NEW] Modular Notebook Cells
- **Cell 1: Environment & Tracing Setup**: Initialize Arize Phoenix and register the `tracer`.
- **Cell 2: Data & Features**: Core preprocessing (CryoSleep constraints, Cabin splitting, etc.).
- **Cell 3: Multi-Model HPO with Tracing**:
    - Implement `objective_catboost`, `objective_xgboost`, and `objective_lgbm`.
    - Integrated with Arize Phoenix for live metric and hyperparameter tracking.
- **Cell 4: Persistent HPO Execution**: 
    - Full Optuna loop with SQLite (`optuna.db`) for all three models.
- **Cell 5: Stacking Ensemble**:
    - Implement a `StackingEnsemble` class.
    - OOF prediction generation and Meta-Model (Logistic Regression) training.
- **Cell 6: Final Inference & Submission**:
    - Multi-seed averaging for final predictions.

## Verification Plan

### Manual Verification
- Provide the code blocks to the user.
- User runs blocks in `Untitled-2.ipynb`.
- Verify traces appear in Phoenix UI with `metric.auc` and `metric.accuracy` / `metric.auf`.
