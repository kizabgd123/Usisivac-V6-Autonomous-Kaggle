#!/usr/bin/env python3
"""
Pairwise Features Module
Creates interaction features between categorical variables.
Source: Chris Deotte's ChatGPT Vibe Coding notebook
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from itertools import combinations
import warnings

warnings.filterwarnings('ignore')


def create_pairwise_interaction(
    df: pd.DataFrame,
    feature1: str,
    feature2: str,
    target_column: Optional[str] = None,
    encoding_type: str = 'frequency'
) -> Tuple[pd.DataFrame, Dict]:
    """
    Create pairwise interaction feature between two categorical variables.
    
    Args:
        df: Input DataFrame
        feature1: First feature name
        feature2: Second feature name
        target_column: Optional target for target-based encoding
        encoding_type: Type of encoding ('frequency', 'target', 'label')
    
    Returns:
        df: DataFrame with new interaction feature
        interaction_info: Dictionary with interaction statistics
    """
    interaction_name = f"{feature1}_x_{feature2}"
    
    # Create raw interaction
    df[interaction_name] = df[feature1].astype(str) + '_' + df[feature2].astype(str)
    
    interaction_info = {
        'features': [feature1, feature2],
        'interaction_name': interaction_name,
        'n_unique_combinations': df[interaction_name].nunique(),
        'encoding_type': encoding_type
    }
    
    # Apply encoding
    if encoding_type == 'frequency':
        freq_map = df[interaction_name].value_counts().to_dict()
        df[f"{interaction_name}_freq"] = df[interaction_name].map(freq_map)
        interaction_info['encoding'] = 'frequency'
        interaction_info['freq_range'] = [
            df[f"{interaction_name}_freq"].min(),
            df[f"{interaction_name}_freq"].max()
        ]
        
    elif encoding_type == 'target' and target_column is not None:
        target_map = df.groupby(interaction_name)[target_column].mean().to_dict()
        df[f"{interaction_name}_te"] = df[interaction_name].map(target_map)
        interaction_info['encoding'] = 'target'
        interaction_info['target_mean_range'] = [
            df[f"{interaction_name}_te"].min(),
            df[f"{interaction_name}_te"].max()
        ]
        
    elif encoding_type == 'label':
        label_map = {v: i for i, v in enumerate(df[interaction_name].unique())}
        df[f"{interaction_name}_lbl"] = df[interaction_name].map(label_map)
        interaction_info['encoding'] = 'label'
        interaction_info['n_labels'] = len(label_map)
    
    # Drop raw interaction
    df = df.drop(columns=[interaction_name])
    
    return df, interaction_info


def create_pairwise_features(
    df: pd.DataFrame,
    feature_pairs: List[Tuple[str, str]],
    target_column: Optional[str] = None,
    encoding_type: str = 'frequency'
) -> Tuple[pd.DataFrame, Dict]:
    """
    Create multiple pairwise interaction features.
    
    Args:
        df: Input DataFrame
        feature_pairs: List of (feature1, feature2) tuples
        target_column: Optional target for target-based encoding
        encoding_type: Type of encoding ('frequency', 'target', 'label')
    
    Returns:
        df: DataFrame with new interaction features
        all_interactions: Dictionary with all interaction statistics
    """
    all_interactions = {}
    
    for feat1, feat2 in feature_pairs:
        if feat1 not in df.columns or feat2 not in df.columns:
            print(f"  ⚠️ Pair ({feat1}, {feat2}) - one or both features not found, skipping...")
            continue
        
        print(f"  🔗 Creating interaction: {feat1} x {feat2}...")
        
        df, info = create_pairwise_interaction(
            df, feat1, feat2, target_column, encoding_type
        )
        
        all_interactions[f"{feat1}_x_{feat2}"] = info
        
        if encoding_type == 'frequency':
            print(f"    ✅ {feat1}_x_{feat2}_freq: {info['n_unique_combinations']} combinations, "
                  f"freq range: {info['freq_range']}")
        elif encoding_type == 'target':
            print(f"    ✅ {feat1}_x_{feat2}_te: {info['n_unique_combinations']} combinations, "
                  f"target mean range: {info['target_mean_range']}")
        else:
            print(f"    ✅ {feat1}_x_{feat2}_lbl: {info['n_unique_combinations']} combinations, "
                  f"{info['n_labels']} labels")
    
    return df, all_interactions


def create_all_pairwise_features(
    df: pd.DataFrame,
    categorical_features: List[str],
    target_column: Optional[str] = None,
    encoding_type: str = 'frequency',
    max_interactions: int = 10
) -> Tuple[pd.DataFrame, Dict]:
    """
    Create all pairwise interactions from a list of categorical features.
    
    Args:
        df: Input DataFrame
        categorical_features: List of categorical feature names
        target_column: Optional target for target-based encoding
        encoding_type: Type of encoding
        max_interactions: Maximum number of interactions to create
    
    Returns:
        df: DataFrame with new interaction features
        all_interactions: Dictionary with all interaction statistics
    """
    # Generate all pairs
    all_pairs = list(combinations(categorical_features, 2))
    
    # Limit if needed
    if len(all_pairs) > max_interactions:
        print(f"  📊 Limiting to {max_interactions} interactions (out of {len(all_pairs)} possible)")
        all_pairs = all_pairs[:max_interactions]
    
    print(f"  📊 Creating {len(all_pairs)} pairwise interactions...")
    
    return create_pairwise_features(df, all_pairs, target_column, encoding_type)


def create_ngram_features(
    df: pd.DataFrame,
    feature_name: str,
    ngram_range: Tuple[int, int] = (2, 3),
    encoding_type: str = 'frequency',
    target_column: Optional[str] = None
) -> Tuple[pd.DataFrame, Dict]:
    """
    Create n-gram style features from a single categorical feature.
    Note: This is for categorical values that contain multiple tokens.
    
    Args:
        df: Input DataFrame
        feature_name: Name of the feature to create n-grams from
        ngram_range: Range of n-grams to create (min_n, max_n)
        encoding_type: Type of encoding
        target_column: Optional target for target-based encoding
    
    Returns:
        df: DataFrame with n-gram features
        ngram_info: Dictionary with n-gram statistics
    """
    ngram_info = {
        'feature': feature_name,
        'ngram_range': ngram_range,
        'encoding_type': encoding_type,
        'features_created': []
    }
    
    # For categorical features, we'll create polynomial-style interactions
    # by combining the feature with itself (squared, cubed terms for numeric encoding)
    
    if encoding_type == 'frequency':
        freq_map = df[feature_name].value_counts().to_dict()
        base_encoded = df[feature_name].map(freq_map)
        
        for n in range(ngram_range[0], ngram_range[1] + 1):
            new_col = f"{feature_name}_freq_pow{n}"
            df[new_col] = np.power(base_encoded, n)
            ngram_info['features_created'].append(new_col)
            print(f"    ✅ Created {new_col}")
    
    return df, ngram_info
