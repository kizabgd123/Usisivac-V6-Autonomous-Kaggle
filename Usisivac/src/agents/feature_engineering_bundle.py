#!/usr/bin/env python3
"""
Feature Engineering Bundle
Unified interface for Chris Deotte's feature engineering techniques.
Integrates: Hill Climbing, Numeric Snapper, Target Encoding, Pairwise Features
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import warnings

from Usisivac.src.agents.numeric_snapper import apply_numeric_snapper, smart_numeric_snapper
from Usisivac.src.agents.target_encoding import apply_target_encoding, target_encode_with_test
from Usisivac.src.agents.pairwise_features import (
    create_pairwise_features,
    create_all_pairwise_features,
    create_pairwise_interaction
)
from Usisivac.src.agents.hill_climbing import (
    hill_climbing_ensemble,
    rank_based_ensemble
)

warnings.filterwarnings('ignore')


class FeatureEngineeringBundle:
    """
    Unified feature engineering bundle for Kaggle competitions.
    Combines proven techniques from Chris Deotte's notebooks.
    """
    
    def __init__(
        self,
        target_column: str = 'Churn',
        numeric_features: Optional[List[str]] = None,
        categorical_features: Optional[List[str]] = None,
        pairwise_features: Optional[List[Tuple[str, str]]] = None
    ):
        self.target_column = target_column
        self.numeric_features = numeric_features or []
        self.categorical_features = categorical_features or []
        self.pairwise_features = pairwise_features or []
        
        self.encoding_stats = {}
        self.snapper_stats = {}
        self.pairwise_stats = {}
    
    def apply_all(
        self,
        df: pd.DataFrame,
        apply_snapper: bool = True,
        apply_target_encoding: bool = True,
        apply_pairwise: bool = True,
        snapper_min_freq: int = 10,
        target_enc_splits: int = 5,
        target_enc_smoothing: float = 1.0
    ) -> Tuple[pd.DataFrame, Dict]:
        """
        Apply all feature engineering techniques.
        
        Args:
            df: Input DataFrame
            apply_snapper: Whether to apply numeric snapper
            apply_target_encoding: Whether to apply target encoding
            apply_pairwise: Whether to apply pairwise features
            snapper_min_freq: Minimum frequency for numeric snapper
            target_enc_splits: Number of CV folds for target encoding
            target_enc_smoothing: Smoothing factor for target encoding
        
        Returns:
            df: Transformed DataFrame
            all_stats: Dictionary with all statistics
        """
        print("\n🔧 Feature Engineering Bundle - Starting...")
        print(f"   Target: {self.target_column}")
        print(f"   Numeric features: {len(self.numeric_features)}")
        print(f"   Categorical features: {len(self.categorical_features)}")
        print(f"   Pairwise features: {len(self.pairwise_features)}")
        print("=" * 50)
        
        all_stats = {}
        
        # 1. Numeric Snapper
        if apply_snapper and self.numeric_features:
            print("\n📌 Step 1: Numeric Snapper")
            df, self.snapper_stats = apply_numeric_snapper(
                df,
                self.numeric_features,
                min_frequency=snapper_min_freq
            )
            all_stats['snapper'] = self.snapper_stats
        
        # 2. Target Encoding
        if apply_target_encoding and self.categorical_features:
            print("\n📌 Step 2: Target Encoding (K-Fold CV)")
            df, self.encoding_stats = apply_target_encoding(
                df,
                self.categorical_features,
                target_column=self.target_column,
                n_splits=target_enc_splits,
                smoothing=target_enc_smoothing
            )
            all_stats['target_encoding'] = self.encoding_stats
        
        # 3. Pairwise Features
        if apply_pairwise and self.pairwise_features:
            print("\n📌 Step 3: Pairwise Interactions")
            df, self.pairwise_stats = create_pairwise_features(
                df,
                self.pairwise_features,
                target_column=self.target_column,
                encoding_type='frequency'
            )
            all_stats['pairwise'] = self.pairwise_stats
        
        print("\n" + "=" * 50)
        print(f"✅ Feature Engineering Complete!")
        print(f"   Final shape: {df.shape}")
        print("=" * 50)
        
        return df, all_stats
    
    def apply_telco_churn_defaults(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
        """
        Apply default feature engineering for Telco Churn competition.
        Based on Chris Deotte's proven techniques.
        """
        # Default features for Telco Churn
        self.numeric_features = ['tenure', 'MonthlyCharges', 'TotalCharges']
        self.categorical_features = [
            'gender', 'SeniorCitizen', 'Partner', 'Dependents',
            'PhoneService', 'MultipleLines', 'InternetService',
            'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
            'TechSupport', 'StreamingTV', 'StreamingMovies',
            'Contract', 'PaperlessBilling', 'PaymentMethod'
        ]
        self.pairwise_features = [
            ('PaymentMethod', 'Contract'),
            ('Contract', 'InternetService'),
            ('InternetService', 'OnlineSecurity')
        ]
        
        return self.apply_all(df)


def dynamic_engineer_features(
    df: pd.DataFrame,
    original_df: Optional[pd.DataFrame] = None,
    target_column: str = 'Churn'
) -> pd.DataFrame:
    """
    Main entry point for dynamic feature engineering.
    This function is called by FeatureAgentV6.
    
    Args:
        df: Input DataFrame (cleaned)
        original_df: Original raw DataFrame (for probability lookups)
        target_column: Target column name
    
    Returns:
        df: DataFrame with engineered features
    """
    print("\n" + "=" * 60)
    print("🚀 DYNAMIC FEATURE ENGINEERING - Chris Deotte Techniques")
    print("=" * 60)
    
    # Identify feature types automatically
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if target_column in numeric_cols:
        numeric_cols.remove(target_column)
    
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    # Key numeric features for snapper
    numeric_snapper_features = [f for f in ['tenure', 'MonthlyCharges', 'TotalCharges'] 
                                 if f in numeric_cols]
    
    # Key categorical features for target encoding
    categorical_te_features = [f for f in categorical_cols 
                                if f not in ['customerID', target_column]]
    
    # Pairwise interactions (proven effective for Telco Churn)
    pairwise_list = [
        ('PaymentMethod', 'Contract'),
        ('Contract', 'InternetService'),
        ('PaymentMethod', 'InternetService')
    ]
    # Filter to only include features that exist
    pairwise_list = [(f1, f2) for f1, f2 in pairwise_list 
                     if f1 in df.columns and f2 in df.columns]
    
    # Initialize bundle
    bundle = FeatureEngineeringBundle(
        target_column=target_column,
        numeric_features=numeric_snapper_features,
        categorical_features=categorical_te_features[:8],  # Limit to top 8
        pairwise_features=pairwise_list
    )
    
    # Apply all techniques
    df, stats = bundle.apply_all(
        df,
        apply_snapper=True,
        apply_target_encoding=True,
        apply_pairwise=True
    )
    
    # Store stats in df.attrs for later reference
    df.attrs['feature_engineering_stats'] = stats
    
    return df
