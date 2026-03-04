import os
import subprocess
import re
from Usisivac.src.agents.base import BaseAgent

class CoderAgentV6(BaseAgent):
    """Refined CoderAgent that ensures the output follows the required interface."""
    
    def __init__(self):
        super().__init__('CoderAgentV6', 'ml')

    def run(self, data, context: dict = None) -> str:
        self.log("🤖 Generating autonomous Feature Engineering code (V6)...")
        
        research = context.get('ResearchAgent', {}).get('findings', '')
        critic = context.get('CriticAgent', {}).get('anti_patterns', '')
        skills = context.get('available_skills', 'No expert skills available.')
        
        # Stricter prompt to ensure the function name matches
        prompt = f"""
        Available Expert Skills:
        {skills}

        Based on the following Research and Critic findings, 
        write a Python function `dynamic_engineer_features(df, original_df=None)`.
        
        RESEARCH: {research[:1500]}
        CRITIC: {critic[:1500]}
        
        STRICT RULES:
        1. Function name MUST be exactly `dynamic_engineer_features(df, original_df=None)`.
        2. Return only the transformed DataFrame.
        3. Do not include ID columns in output.
        4. Handle TotalCharges.
        5. Output ONLY the code block starting with 'def dynamic_engineer_features'.
        """
        
        try:
            with open("Usisivac/tmp_prompt_v6.txt", "w") as f:
                f.write(prompt)
            
            cmd = "python3 Usisivac/src/generate_report.py \"Write the python function dynamic_engineer_features(df, original_df=None) based on Usisivac/tmp_prompt_v6.txt. No talk, just code.\""
            raw_output = subprocess.check_output(cmd, shell=True, text=True)
            
            # More aggressive cleaning of the output
            code = raw_output
            if "```python" in code:
                code = re.search(r"```python\n(.*?)```", code, re.DOTALL).group(1)
            elif "```" in code:
                code = re.search(r"```\n(.*?)```", code, re.DOTALL).group(1)
            
            # Prepend necessary imports
            final_code = "import pandas as pd\nimport numpy as np\nimport re\n\n" + code
            
            with open("Usisivac/src/agents/generated_features.py", "w") as f:
                f.write(final_code)
            
            self.log("✅ Autonomous Code V6 saved to Usisivac/src/agents/generated_features.py")
            self.state = {'generated_code_path': "Usisivac/src/agents/generated_features.py"}
            
        except Exception as e:
            self.log(f"❌ Code Generation Failed: {e}", level='ERROR')
            
        return data
