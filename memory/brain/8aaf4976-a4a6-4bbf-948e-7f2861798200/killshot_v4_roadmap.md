# Strategic Roadmap: Killshot V4

## 🎯 Primary Goal
Transition from a redundant ensemble to an **Orthogonal Hybrid System** with superior calibration and uncertainty awareness.

## 🚀 Key Modules

### 1. Diversity-First Ensembling
*   **Feature Subspacing**: Train models on non-overlapping clinical feature sets (e.g., Blood Chemistry vs. Physiological Stress).
*   **Meta-Learner**: Replace simple blending with a **Bayesian Meta-Learner** or a calibrated Logistic Regression to learn model strengths.

### 2. SOTA Calibration Layer
*   **Isotonic Pass**: Apply Isotonic Regression on OOF probabilities to ensure reported AUC reflects true probability reliability.
*   **Reliability Plots**: Mandatory automated artifact for every v4 sub-system.

### 3. Uncertainty-Aware Denoising
*   **Soft Weights**: Instead of hard-dropping 15k rows, apply weights inversely proportional to Cleanlab's "self-confidence" score.
*   **Synthetic Reinjection**: Re-introduce a small percentage of high-signal synthetic rows previously flagged as "uncertain" but corrected by UCI anchor.

---

## 📅 Roadmap Phases

| Phase | Task | ROI |
| :--- | :--- | :--- |
| **I: Orthogonality** | Implement `FeatureSubspacing` | High (Reduces Correlation) |
| **II: Calibration** | Add `IsotonicCalibration` | Medium (Improves Reliability) |
| **III: Soft Denoising** | Shift to `SoftPruning` | Medium (Preserves Signal) |

## ✅ System Readiness
- [x] ProcessGuard Hardened (Rule 10)
- [x] MemoryIntegrity Optimized (Rule 27)
- [ ] V4 Framework Shell
