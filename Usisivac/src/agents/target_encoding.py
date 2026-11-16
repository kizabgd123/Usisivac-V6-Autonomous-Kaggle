#!/usr/bin/env python3
"""
Target Encoding Module with K-Fold Cross-Validation
Prevents data leakage by using out-of-fold encoding for training data.
Source: Chris Deotte's notebooks
"""

import json
import os
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import KFold, StratifiedKFold
from typing import Dict, List, Tuple, Optional
import warnings

warnings.filterwarnings('ignore')




def _validate_pre_registered_smoothing(smoothing: float) -> None:
    """Require smoothing to match the committed experiment plan before outer CV."""
    try:
        value = float(smoothing)
    except (TypeError, ValueError) as exc:
        raise ValueError("Target-encoding smoothing must be a finite positive number") from exc
    if not np.isfinite(value) or value <= 0:
        raise ValueError("Target-encoding smoothing must be a finite positive number")

    project_root = Path(__file__).resolve().parents[3]
    plan_path = Path(os.environ.get(
        "USISIVAC_EXPERIMENT_PLAN",
        str(project_root / "eval" / "experiment_plan.json")
    ))
    try:
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
        policy = plan["target_encoding"]
        registered = float(policy["smoothing"])
        is_registered = (
            plan.get("status") == "pre_registered"
            and plan.get("registered_before_evaluation") is True
            and policy.get("policy") == "pre_registered"
        )
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        raise ValueError(f"Cannot verify target-encoding plan {plan_path}: {exc}") from exc
    if not is_registered:
        raise ValueError("Target-encoding smoothing must be pre-registered before outer CV")
    if not np.isclose(value, registered, rtol=0.0, atol=1e-12):
        raise ValueError(
            f"smoothing={value} is not pre-registered (plan value={registered}); "
            "do not tune against outer validation AUC"
        )


def target_encode_feature(
    train_series: pd.Series,
    train_target: pd.Series,
    val_series: pd.Series = None,
    test_series: pd.Series = None,
    n_splits: int = 5,
    smoothing: float = 1.0,
    random_state: int = 42
) -> Tuple[pd.Series, Optional[pd.Series], Optional[pd.Series], Dict]:
    """
    Apply target encoding to a single categorical feature using K-Fold CV.
    
    Args:
        train_series: Training feature series
        train_target: Training target series
        val_series: Validation feature series (optional)
        test_series: Test feature series (optional)
        n_splits: Number of CV folds
        smoothing: Smoothing factor to handle rare categories
        random_state: Random seed
    
    Returns:
        train_encoded: Encoded training series
        val_encoded: Encoded validation series (if provided)
        test_encoded: Encoded test series (if provided)
        encoding_info: Dictionary with encoding statistics
    """
    _validate_pre_registered_smoothing(smoothing)

    # Full outer-training statistics are used only for external validation/test mapping.
    global_mean = train_target.mean()
    
    # Calculate target statistics per category
    agg = train_target.groupby(train_series).agg(['mean', 'count'])
    agg.columns = ['target_mean', 'count']
    
    # Apply smoothing
    smoothing_factor = 1 / (1 + np.exp(-(agg['count'] - 1) / smoothing))
    agg['smoothed_mean'] = agg['target_mean'] * smoothing_factor + global_mean * (1 - smoothing_factor)
    
    # For training data: use out-of-fold encoding
    train_encoded = np.zeros(len(train_series))
    
    kfold = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=random_state)
    
    for fold_idx, (train_idx, val_idx) in enumerate(kfold.split(train_series, train_target)):
        # Calculate encoding and smoothing prior on this fold's training rows only.
        fold_train = train_series.iloc[train_idx]
        fold_target = train_target.iloc[train_idx]
        fold_global_mean = fold_target.mean()
        
        fold_agg = fold_target.groupby(fold_train).agg(['mean', 'count'])
        fold_agg.columns = ['target_mean', 'count']
        
        # Apply smoothing
        fold_smoothing = 1 / (1 + np.exp(-(fold_agg['count'] - 1) / smoothing))
        fold_agg['smoothed_mean'] = fold_agg['target_mean'] * fold_smoothing + fold_global_mean * (1 - fold_smoothing)
        
        # Map to validation fold
        train_encoded[val_idx] = train_series.iloc[val_idx].map(fold_agg['smoothed_mean']).fillna(fold_global_mean)
    
    train_encoded = pd.Series(train_encoded, index=train_series.index, name=f"{train_series.name}_te")
    
    # For validation and test: use full training encoding
    val_encoded = None
    if val_series is not None:
        val_encoded = val_series.map(agg['smoothed_mean']).fillna(global_mean)
        val_encoded = pd.Series(val_encoded, index=val_series.index, name=f"{val_series.name}_te")
    
    test_encoded = None
    if test_series is not None:
        test_encoded = test_series.map(agg['smoothed_mean']).fillna(global_mean)
        test_encoded = pd.Series(test_encoded, index=test_series.index, name=f"{test_series.name}_te")
    
    encoding_info = {
        'feature': train_series.name,
        'n_categories': len(agg),
        'global_mean': global_mean,
        'min_category_count': agg['count'].min(),
        'max_category_count': agg['count'].max(),
        'smoothing': smoothing
    }
    
    return train_encoded, val_encoded, test_encoded, encoding_info


def apply_target_encoding(
    df: pd.DataFrame,
    categorical_features: List[str],
    target_column: str = 'Churn',
    n_splits: int = 5,
    smoothing: float = 1.0,
    suffix: str = '_te',
    random_state: int = 42
) -> Tuple[pd.DataFrame, Dict]:
    """
    Apply target encoding to multiple categorical features.
    
    Args:
        df: Input DataFrame with target column
        categorical_features: List of categorical feature names
        target_column: Name of target column
        n_splits: Number of CV folds
        smoothing: Smoothing factor
        suffix: Suffix for encoded feature names
        random_state: Random seed
    
    Returns:
        df: DataFrame with target-encoded features added
        all_encoding_info: Dictionary with all encoding statistics
    """
    all_encoding_info = {}
    
    for feature in categorical_features:
        if feature not in df.columns:
            print(f"  ⚠️ Feature '{feature}' not found, skipping...")
            continue
        
        print(f"  🔧 Target encoding: {feature}...")
        
        encoded, _, _, info = target_encode_feature(
            df[feature],
            df[target_column],
            n_splits=n_splits,
            smoothing=smoothing,
            random_state=random_state
        )
        
        new_feature_name = f"{feature}{suffix}"
        df[new_feature_name] = encoded.values
        
        all_encoding_info[feature] = info
        print(f"    ✅ {feature}: {info['n_categories']} categories, "
              f"count range: [{info['min_category_count']}, {info['max_category_count']}]")
    
    return df, all_encoding_info


def target_encode_with_test(
    train_df: pd.DataFrame,
    test_df: pd.DataFrame,
    categorical_features: List[str],
    target_column: str = 'Churn',
    n_splits: int = 5,
    smoothing: float = 1.0,
    random_state: int = 42
) -> Tuple[pd.DataFrame, pd.DataFrame, Dict]:
    """
    Apply target encoding to train and test sets.
    
    Args:
        train_df: Training DataFrame
        test_df: Test DataFrame
        categorical_features: List of categorical feature names
        target_column: Name of target column in train_df
        n_splits: Number of CV folds
        smoothing: Smoothing factor
        random_state: Random seed
    
    Returns:
        train_df: Training DataFrame with encoded features
        test_df: Test DataFrame with encoded features
        all_encoding_info: Dictionary with encoding statistics
    """
    all_encoding_info = {}
    
    for feature in categorical_features:
        if feature not in train_df.columns or feature not in test_df.columns:
            print(f"  ⚠️ Feature '{feature}' not in both datasets, skipping...")
            continue
        
        print(f"  🔧 Target encoding: {feature}...")
        
        train_encoded, _, test_encoded, info = target_encode_feature(
            train_df[feature],
            train_df[target_column],
            test_series=test_df[feature],
            n_splits=n_splits,
            smoothing=smoothing,
            random_state=random_state
        )
        
        train_df[f"{feature}_te"] = train_encoded.values
        test_df[f"{feature}_te"] = test_encoded.values
        
        all_encoding_info[feature] = info
    
    return train_df, test_df, all_encoding_info
