# Shot 3: Elite Snippets v3.3 (CPU/Fix)

This plan provides modular code blocks to fix the CV/LB gap and implement Geometric Fusion without requiring GPU.

## I. MICE Hardening (Fixes CV/LB Gap)

**Issue:** `mice.fit(combined)` leaks test distribution.
**Fix:** Fit only on `train`.

```python
# Replace your MICE block with this:
mice = IterativeImputer(max_iter=10, random_state=42)
print("  Fitting MICE on TRAIN ONLY...")
mice.fit(train[impute_cols])

print("  Transforming Train & Test...")
train[impute_cols] = mice.transform(train[impute_cols])
test[impute_cols]  = mice.transform(test[impute_cols])
```

## II. Geometric Fusion (Target: 0.9575+)

Instead of `np.mean()`, use geometric mean of sorted ranks. This is more stable for CPU-trained models that might not be perfectly calibrated.

```python
from scipy.stats import rankdata

def geometric_rank_fusion(preds_list):
    """
    preds_list: List of 1D arrays of probabilities
    """
    all_ranks = []
    for p in preds_list:
        # Convert probabilities to ranks (0 to 1)
        ranks = rankdata(p) / len(p)
        all_ranks.append(ranks)
    
    # Geometric mean of ranks
    fused_ranks = np.exp(np.mean([np.log(r) for r in all_ranks], axis=0))
    return fused_ranks
```

## III. CPU-Optimized Model Strategy

Since GPU is unavailable, use **HistGradientBoostingClassifier** and **LGBM** with small learning rates but deeper trees.

- **HistGB**: Native support for missing values (less dependent on MICE).
- **LGBM**: Use `device='cpu'` and `num_leaves=63` for better signal on small CPU runs.
