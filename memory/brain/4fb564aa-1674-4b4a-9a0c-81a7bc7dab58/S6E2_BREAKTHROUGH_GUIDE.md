# S6E2 Heart Disease Breakthrough Guide

## Overview
This guide documents the "fundamental shift" required to move beyond incremental GBDT improvements (XGB/LGB/CAT) which typically saturate at ~0.9538 Public LB due to high local redundancy (correlations >0.99).

## Key Pillars of Diversity

### 1. Tabular Neural Networks (Non-GBDT)
- **RealMLP**: Strongest solo non-GBDT performer.
- **FT-Transformer**: Attention-based feature extraction.
- **TabNet**: Sparse attention-based model.
> [!TIP]
> Blending these (0.3-0.4 weight) with GBDTs addresses the "averaging noise" issue by introducing orthogonal signals.

### 2. The "Original Data Secret"
- **Dataset**: UCI Heart Disease (270-303 rows).
- **Techniques**: 
  - Target Statistics (Mean/Std/Skew) from original data only.
  - Careful concatenation (concatenating real rows with synthetic).
  - Two-stage training (Pre-train on real -> Fine-tune on synthetic).

### 3. Regime-Structured Models
- **Concept**: Split patients into latent zones (e.g., by `vessels_fluro` and `thallium`).
- **Discovery**: In ~9% of high-risk patients, metabolic factors (Age/Lipids) override traditional symptoms (Chest Pain).
- **Execution**: Specialised zone-based Random Forests or extra meta-features.

## Quick-Start Roadmap
1. **Augment**: Add UCI target statistics to your training set.
2. **Train**: Run a 5-fold RealMLP.
3. **AutoML**: Execute AutoGluon `best_quality` for automatic ensemble diversity.
4. **Blend**: Simple weighted average or Ridge/LR meta-learner.

## Why This Works
GBDTs are restricted to axis-aligned splits on the same synthetic rows. NNs use embeddings and attention to see "between the lines," while real UCI data corrects GAN artifacts in the 630k synthetic set.
