import os
import pandas as pd
import numpy as np
from Usisivac.src.agents.base import BaseAgent

class FeatureAgentV6(BaseAgent):
    """Dynamic Feature Engineering using auto-generated code."""
    
    def __init__(self, original_df_path: str = "data/original.csv"):
        super().__init__('FeatureAgentV6', 'default')
        self.original_df_path = original_df_path

    def run(self, df: pd.DataFrame, context: dict = None) -> pd.DataFrame:
        self.log("⚙️ Executing Autonomous Feature Engineering...")
        
        # Load the generated code
        # We'll use exec() to run the function in this scope
        try:
            with open("Usisivac/src/agents/generated_features.py", "r") as f:
                code = f.read()
            
            # Create a dictionary to hold the function
            namespace = {}
            # Import dependencies that might be needed
            namespace['pd'] = pd
            namespace['np'] = np
            import re
            namespace['re'] = re
            from sklearn.preprocessing import LabelEncoder
            namespace['LabelEncoder'] = LabelEncoder
            
            exec(code, namespace)
            
            if 'dynamic_engineer_features' in namespace:
                engineer_func = namespace['dynamic_engineer_features']
                
                # Load original data if available
                original_df = None
                if os.path.exists(self.original_df_path):
                     original_df = pd.read_csv(self.original_df_path)
                     self.log(f"✅ Loaded original data for probability lookups: {self.original_df_path}")
                
                # Execute the dynamic function
                df = engineer_func(df, original_df)
                self.log(f"✅ Autonomous Engineering Applied — final shape: {df.shape}")
                self.state = {'applied_features': df.columns.tolist()}
            else:
                self.log("❌ Error: 'dynamic_engineer_features' function not found in generated code.", level='ERROR')
                
        except Exception as e:
            self.log(f"❌ Error executing autonomous code: {e}", level='ERROR')
            
        return df
