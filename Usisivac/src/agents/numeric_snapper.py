#!/usr/bin/env python3
"""
Numeric Snapper Module
Snaps rare numeric values to nearest frequent neighbors to reduce noise.
Source: Chris Deotte's notebooks
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
import warnings

warnings.filterwarnings('ignore')


def calculate_value_frequencies(
    series: pd.Series,
    min_frequency: int = 10
) -> pd.Series:
    """
    Calculate value frequencies and identify rare values.
    
    Args:
        series: Input numeric series
        min_frequency: Minimum frequency for a value to be considered common
    
    Returns:
        Frequency counts for each unique value
    """
    value_counts = series.value_counts()
    return value_counts[value_counts >= min_frequency]


def snap_to_frequent(
    series: pd.Series,
    feature_name: str,
    min_frequency: int = 10,
    n_neighbors: int = 5
) -> Tuple[pd.Series, Dict]:
    """
    Snap rare values to nearest frequent neighbors.
    
    Args:
        series: Input numeric series
        feature_name: Name of the feature for logging
        min_frequency: Minimum frequency for common values
        n_neighbors: Number of nearest neighbors to consider
    
    Returns:
        snapped_series: Series with rare values snapped
        snap_info: Dictionary with snapping statistics
    """
    # Get frequent values
    freq_values = calculate_value_frequencies(series, min_frequency)
    
    if len(freq_values) == 0:
        # No frequent values, return original
        return series, {'snapped_count': 0, 'frequent_values': []}
    
    frequent_set = set(freq_values.index)
    sorted_frequent = sorted(freq_values.index)
    
    snapped_values = series.copy()
    snapped_count = 0
    
    # For each unique value in the series
    for unique_val in series.unique():
        if unique_val not in frequent_set:
            # Find nearest frequent neighbor
            distances = [abs(unique_val - fv) for fv in sorted_frequent]
            nearest_idx = np.argmin(distances)
            nearest_val = sorted_frequent[nearest_idx]
            
            # Snap to nearest
            snapped_values[series == unique_val] = nearest_val
            snapped_count += (series == unique_val).sum()
    
    snap_info = {
        'feature': feature_name,
        'snapped_count': snapped_count,
        'snapped_pct': snapped_count / len(series) * 100,
        'original_unique_count': series.nunique(),
        'snapped_unique_count': snapped_values.nunique(),
        'frequent_values': sorted_frequent
    }
    
    return snapped_values, snap_info


def apply_numeric_snapper(
    df: pd.DataFrame,
    numeric_features: List[str],
    min_frequency: int = 10,
    n_neighbors: int = 5,
    suffix: str = '_snapped'
) -> Tuple[pd.DataFrame, Dict]:
    """
    Apply numeric snapper to multiple features.
    
    Args:
        df: Input DataFrame
        numeric_features: List of numeric feature names to snap
        min_frequency: Minimum frequency for common values
        n_neighbors: Number of nearest neighbors
        suffix: Suffix for new feature names
    
    Returns:
        df: DataFrame with snapped features added
        all_snap_info: Dictionary with all snapping statistics
    """
    all_snap_info = {}
    
    for feature in numeric_features:
        if feature not in df.columns:
            print(f"  ⚠️ Feature '{feature}' not found, skipping...")
            continue
        
        new_feature_name = f"{feature}{suffix}"
        
        snapped_values, snap_info = snap_to_frequent(
            df[feature],
            feature_name=feature,
            min_frequency=min_frequency,
            n_neighbors=n_neighbors
        )
        
        df[new_feature_name] = snapped_values
        all_snap_info[feature] = snap_info
        
        print(f"  ✅ {feature}: Snapped {snap_info['snapped_count']} values "
              f"({snap_info['snapped_pct']:.1f}%), "
              f"unique: {snap_info['original_unique_count']} → {snap_info['snapped_unique_count']}")
    
    return df, all_snap_info


def smart_numeric_snapper(
    df: pd.DataFrame,
    target_column: str = 'Churn',
    min_frequency: int = 10,
    correlation_threshold: float = 0.05
) -> Tuple[pd.DataFrame, Dict]:
    """
    Smart numeric snapper that only snaps features correlated with target.
    
    Args:
        df: Input DataFrame with target column
        target_column: Name of target column
        min_frequency: Minimum frequency for common values
        correlation_threshold: Minimum correlation with target to consider
    
    Returns:
        df: DataFrame with snapped features
        snap_results: Dictionary with snapping results
    """
    # Find numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if target_column in numeric_cols:
        numeric_cols.remove(target_column)
    
    # Calculate correlations with target
    correlations = {}
    for col in numeric_cols:
        corr = df[col].corr(df[target_column])
        if abs(corr) > correlation_threshold:
            correlations[col] = corr
    
    print(f"  📊 Found {len(correlations)} numeric features with correlation > {correlation_threshold}")
    
    # Apply snapper to correlated features
    df, snap_results = apply_numeric_snapper(
        df,
        list(correlations.keys()),
        min_frequency=min_frequency
    )
    
    return df, snap_results
