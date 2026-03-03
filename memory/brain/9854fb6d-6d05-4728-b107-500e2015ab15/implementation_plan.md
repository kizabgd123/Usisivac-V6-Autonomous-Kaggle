# Trinity Protocol Audit & Elite Strategy v9 Implementation Plan

This plan outlines the steps to conduct a constitutional audit of the Trinity Protocol ecosystem and implementation of the "Elite Strategy v9" as defined in the previous task list.

## User Review Required

> [!IMPORTANT]
> **UCI Dataset Integration**: I will be integrating the original UCI Heart Disease dataset to improve model robustness. This has been noted as a potential source of "noise dilution" in the previous task list.
> **Elite Techniques**: I am moving forward with Periodic Embeddings and OOF Target Encoding as these are high-impact SOTA techniques for tabular data.

## Proposed Changes

### Constitutional Fixes & Alignment

#### [MODIFY] [original_data_loader.py](file:///home/kizabgd/Desktop/Istrazivanje/scripts/original_data_loader.py)
- Fix `NameError: name 'dataset_ref' is not defined` on line 15.
- Hardcode the UCI dataset reference or resolve it from config.

#### [MODIFY] [training_pipeline.py](file:///home/kizabgd/Desktop/Istrazivanje/scripts/training_pipeline.py)
- Update `add_golden_features` to support the new elite transformations if signaled.
- Ensure `use_original` correctly triggers the (fixed) `merge_original_data`.

---

### Elite Strategy v9 Implementation

#### [MODIFY] [tool_registry.py](file:///home/kizabgd/Desktop/Istrazivanje/scripts/tool_registry.py)
- Implement `periodic_embedding` tool for `Age` and `MaxHR`.
- Implement `oof_target_encoder` tool for high-cardinality categorical features (`ChestPainType`, etc.).

#### [NEW] [heart_disease_v9_elite.py](file:///home/kizabgd/Desktop/Istrazivanje/scripts/heart_disease_v9_elite.py)
- Main execution script for the v9 strategy.
- Uses `TrainingPipeline` with `use_original=True`.
- Integrates the new tools from `tool_registry.py`.
- Implements the Logistic Regression Stacking meta-model.

## Verification Plan

### Automated Tests
- Run `python3 scripts/verify_components.py` to ensure core registry and memory stability.
- Run `python3 scripts/heart_disease_v9_elite.py` (dry run or limited iterations) to verify the data flow and stacking logic.

### Manual Verification
- Review `GUARD_LOG.md` after training to ensure no VETO/HALT events were triggered.
- Verify that `submission_v9_elite.csv` is generated with valid ranges and count.
