import pandas as pd
import numpy as np
from Usisivac.src.agents.base import BaseAgent

class CleanerAgent(BaseAgent):
    """Automates data cleaning: outlier handling, missing value imputation, and type normalization."""
    
    def __init__(self, outlier_z: float = 3.0):
        super().__init__('CleanerAgent', 'cleaner')
        self.outlier_z = outlier_z

    def run(self, df: pd.DataFrame, context: dict = None) -> pd.DataFrame:
        self.log(f"🧹 Starting data cleaning (Outlier Z-score: {self.outlier_z})...")
        
        # 1. Handle TotalCharges (Telco-specific breakthrough)
        if 'TotalCharges' in df.columns:
            df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
            df['TotalCharges'] = df['TotalCharges'].fillna(0)
            self.log("✅ Normalized 'TotalCharges' (numeric conversion + 0 imputation).")

        # 2. Basic Imputation for numeric columns
        num_cols = df.select_dtypes(include=[np.number]).columns
        for col in num_cols:
            if df[col].isnull().sum() > 0:
                df[col] = df[col].fillna(df[col].median())
        
        # 3. Basic Imputation for categorical columns
        cat_cols = df.select_dtypes(include=['object']).columns
        for col in cat_cols:
            if df[col].isnull().sum() > 0:
                df[col] = df[col].fillna(df[col].mode()[0])

        # 4. Outlier Clipping
        for col in num_cols:
            mean = df[col].mean()
            std = df[col].std()
            limit = self.outlier_z * std
            df[col] = df[col].clip(lower=mean - limit, upper=mean + limit)

        self.log(f"✅ Data cleaning complete. Final shape: {df.shape}")
        self.state = {'cleaning_stats': df.describe().to_dict()}
        
        return df
