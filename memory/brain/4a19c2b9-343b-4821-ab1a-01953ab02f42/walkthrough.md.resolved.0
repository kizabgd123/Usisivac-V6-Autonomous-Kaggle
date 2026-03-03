# Notebook Rewrite — Walkthrough

## What Changed

The notebook `heart-disease-s6e2-lessons-learned` was completely restructured based on 4 reviewer feedback items.

### 1. Structural Inversion ✅
- **Before:** Chronological diary — failures described in order, key takeaways buried in Chapter 8
- **After:** Thesis stated in the first paragraph ("On synthetic data, simple ensembles outperform complex techniques"), followed by numbered evidence sections. Summary findings moved to the opening.

### 2. Pseudo-Labeling Leakage Mechanism ✅
- **Before:** One paragraph saying "predictions leaked into our cross-validation structure"
- **After:** Dedicated section with two pseudocode blocks showing exactly:
  - The **wrong** pipeline (pseudo-labels generated before fold split)
  - The **correct** pipeline (pseudo-labels generated inside each fold)
  - Explanation of *why* the leak occurs and why even the correct version doesn't help on this data

### 3. Clinical Context for Feature Engineering ✅
- **Before:** Tanaka formula shown as a chart with "it's more accurate"
- **After:** Full medical context including:
  - Chronotropic incompetence definition and clinical threshold (0.85)
  - Literature references (Tanaka 2001 meta-analysis, Lauer 1999)
  - Why Fox formula lacks empirical basis
  - Oldpeak as ST depression: clinical significance of the 1mm threshold
  - Ischemic Burden composite as a clinical marker with age-interaction reasoning
  - Why synthetic data specifically may benefit from clinically-derived features

### 4. TabNet/Neural Network Evidence ✅
- **Before:** "you'd need neural nets" with zero evidence
- **After:** New "Discussion" section covering:
  - *Why* GBDTs converge on synthetic data (axis-aligned splits on smooth distributions)
  - TabNet attention mechanism: how instance-specific feature selection differs from global splits
  - FT-Transformer: feature-as-token embedding with self-attention
  - Preliminary result: TabNet-GBDT correlation ~0.87 (vs inter-GBDT ~0.99)
  - Honest acknowledgment: "We did not pursue this far enough to report a definitive result"
  - Code sketch for future experimentation
  - References to Rubachev et al. 2024 and McElfresh et al. 2023

### 5. Tone Cleanup ✅
- Removed all boasting language ("cracked it", "SOTA", etc.)
- Changed chapter titles from "Everything we got wrong" to evidence-based labels
- Added explicit "Open questions we did not resolve" section
- Closing line is humble: "We hope the detailed failure analysis is useful"

## Verification

- **Kaggle push:** v2 successfully pushed → [Link](https://www.kaggle.com/kiza123123/heart-disease-s6e2-lessons-learned)
