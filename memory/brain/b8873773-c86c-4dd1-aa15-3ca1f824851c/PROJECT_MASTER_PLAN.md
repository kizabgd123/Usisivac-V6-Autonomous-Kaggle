# 🕵️ Trinity: Project Master Plan

**Date:** 2026-02-17
**Status:** 🟡 PARTIAL (Phase 2 Complete, Phase 3 In Progress)
**Target:** Kaggle Gold / SOTA (MAE < 10.0)

## 1. Executive Summary
The project has successfully established a strong baseline using Gradient Boosting on RDKit descriptors and exact lookups (Bradley + PubChem), achieving a Public LB MAE of ~14.05. However, we are hitting the limits of "feature engineering" and need to transition to "representation learning" (GNNs) and "massive external data" (Phase 3) to break the 10.0 MAE barrier.

## 2. The "Working" Layer
These components are battle-tested and contributing to the current score:
- **Lookup Pipeline**: `pubchem_lookup.py` and `external_lookup.py` (Bradley dataset) are solid.
- **RDKit Descriptors**: `engineer_rdkit_descriptors.py` generates ~200 reliable 2D features.
- **GBM Stack**: `train_lgbm.py`, `train_xgb_final.py`, and `grandmaster_stack.py` provide the current best model.

## 3. Gap Analysis & Zombie Code
### ⚠️ Zombie Code (Consolidate or Delete)
- **Fragmentation**: Too many training scripts: `train_baseline.py`, `train_v2.py`, `train_layer1.py`, `train_layer2.py`. **Action**: Consolidate into a modular `train_manager.py` or strict Phase-based naming.
- **Redundant Features**: `engineer_mega_features.py` vs `engineer_physical.py` vs `engineer_rdkit_descriptors.py`. **Action**: Unify into `src/features/`.

### 🚨 Critical Blockers
1.  **Phase 3 Data Merge Incomplete**: We have OCHEM (`smiles_melting_point.csv`) and Bradley, but `phase3_clean_and_merge.py` is not yet the single source of truth for the training dataset. We need a unified `gold_train.csv`.
2.  **No GNN Pipeline**: `phase4_gnn_pretrain.py` is present but unverified/incomplete. Deep learning is essential for the next leap.

## 4. End-to-End Roadmap (The "Killshot" Path)

### Phase 3: The Data Scale-Up (Immediate Priority)
- [ ] **Finalize Inspection**: Confirm OCHEM units and Bradley outliers.
- [ ] **Unified Merge**: Create `data/gold/train_v4.csv` combining Train + Bradley + OCHEM (deduplicated).
- [ ] **Salt Stripping**: Ensure robust SMILES cleaning (already partially in `canonicalize_smiles.py`).

### Phase 4: Representation Learning (GNN)
- [ ] **Graph Dataset**: Convert `gold_train.csv` to PyTorch Geometric `InMemoryDataset`.
- [ ] **Pretraining**: Train GIN/GCN on the massive unlabelled/labelled set.
- [ ] **Finetuning**: Finetune on the high-quality Kaggle Train set.

### Phase 5: Trinity Ensemble
- [ ] **Level 1**: LightGBM (RDKit) + XGBoost (RDKit) + GNN (Graph).
- [ ] **Level 2**: Ridge/Bayesian Stacking of Level 1 predictions.
- [ ] **Uncertainty**: Use GNN dropout or Ensemble variance to weight predictions.

## 5. Execution Order
1.  **ACTIVATE** Phase 3 Merge (Finish `scripts/inspect_phase3_data.py` -> `merge_phase3.py`).
2.  **AUDIT** `phase4_gnn_pretrain.py` and make it functional.
3.  **TRAIN** GNN and submit single-model GNN.
4.  **STACK**.
