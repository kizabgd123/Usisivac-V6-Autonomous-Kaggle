# Deep Past - Akkadian Translation Audit

- [x] Fix Gemma CSV parsing corruption (V17)
- [x] Analyze submission failures (COMPLETE but no score)
- [x] Pull verified working kernel `00ecb6`
- [x] Upgrade working kernel with Beam Search (beams=5)
- [x] Upgrade working kernel with Lexicon post-processing
- [x] Push V2.0 SOTA upgrade to Kaggle

# Heart Disease - Tactics Research

- [x] Implement V10.14 SOTA Upgrade
    - [x] Add `scrub_flipped_labels` logic
    - [x] Implement Gaussian Periodic Embeddings
    - [x] Update interactions (remove rank mults)
    - [x] Run 10-fold CV & Validate OOF
- [x] Push V10.14 to Kaggle
- [x] Optimize V10.14 for Google Colab (Auto-Path detection)
- [x] Implement Grandmaster Speed Optimizations (2-3x faster)
    - [x] Update Config (5-fold, 3-seed, LR=0.02)
    - [x] Optimize MLP embedding (cache & n_freqs=8)
    - [x] Convert to NumPy arrays (float32) for XGB/LGB
    - [x] Implement Selective Pseudo-Labeling
    - [x] FIX: CatBoost Feature Alignment & Allocation

# Reviewing Heart Pipeline V10.13 Fixes



- [x] Check Bug #1 fix: CatBoost using fold-specific `X_ho` and `X_te` with TE columns
- [x] Check Bug #2 fix: Pseudo-Label logic preferring higher holdout AUC over raw count
- [x] Check Bug #3 fix: Mutual Information threshold changed (e.g., from 0.001 to 0.005+)
- [x] Check Bug #4 fix: Logistic Regression meta-learner includes C=0.1
- [x] Check Bug #5 fix: Blend weights are dynamically optimized or improved
