# Melting Point Medal Strategy execution

## Phase 1: External SMILES Database Lookup (Gold Path)
- [x] Download Jean-Claude Bradley Open Melting Point Dataset (DPG, 3041 entries)
- [x] Canonicalize all SMILES (train, test, external)
- [x] Match test SMILES → external Tm values (Bradley: 290/666 matches)
- [x] Build hybrid submission v1 (lookup + Ridge fallback) -> **MAE 20.90**
- [x] PubChem Batch Lookup (Phase 1b)
    - [x] Query 376 unmatched SMILES via PUG-REST API
    - [x] Found 137 additional matches
    - [x] Merge into v2 submission -> **MAE 17.94** (Public 14.73)
- [x] **NEXT:** Maximize external data coverage (try OCHEM/DeepChem?) or move to Phase 2?

## Phase 2: Rich RDKit Descriptors (Silver Insurance)
- [x] Generate full RDKit 2D descriptor set (~200 features)
- [x] Retrain GBDT ensemble with enriched features (CV 27.76)
- [x] Re-blend and submit (v3) -> **MAE 17.63** (Public 14.05)


## Phase 3: The Big Data Foundation (Local Execution)
- [x] **Data Hygiene Engine** (`scripts/phase3_clean_and_merge.py`)
    - [x] Implement robust SMILES canonicalization & Salt Stripping
    - [x] Implement "Median Aggregation" for duplicate external entries
    - [x] **CRITICAL:** Filter out ALL Kaggle Test Cluster molecules from training data
    - [x] Generate `data/gold/pretrain_dataset.csv` (276k+, unlabeled OK)
    - [ ] Generate `data/gold/finetune_dataset.csv` (High-confidence labeled)

## Phase 4: Representation Learning (Kaggle T4 Execution)
- [ ] **Phase 4A: Self-Supervised Pretraining**
    - [ ] Create `notebooks/phase4_gnn_pretrain.ipynb`
    - [ ] Implement GIN/AttentiveFP with Masked Atom Prediction
- [ ] **Phase 4B: Supervised Fine-Tuning**
    - [ ] Create `notebooks/phase4_gnn_finetune.ipynb`
    - [ ] Implement Transfer Learning from 4A weights
    - [ ] Train with Huber Loss & Scaffold Split CV

## Phase 5: Trinity Ensemble
- [ ] Develop Uncertainty-Aware Stacking logic
- [ ] Submission v4 (The Killshot)
