import os
import subprocess
from Usisivac.src.agents.base import BaseAgent

class CriticAgent(BaseAgent):
    """Specialized agent to identify anti-patterns, common mistakes, and misconceptions."""
    
    def __init__(self, query: str = "Common mistakes, anti-patterns, and misconceptions in Telco Churn prediction and Kaggle Playground S6E3"):
        super().__init__('CriticAgent', 'guardian')
        self.query = query

    def run(self, data, context: dict = None) -> dict:
        self.log(f"🛡️ Auditing Knowledge Base for Anti-Patterns: '{self.query}'...")
        
        try:
            # Call the RAG system to find what NOT to do
            cmd = f"python3 Usisivac/src/generate_report.py '{self.query}'"
            result = subprocess.check_output(cmd, shell=True, text=True)
            self.log("✅ Anti-Pattern Audit Complete.")
            
            # Store in state
            self.state = {'anti_patterns': result, 'query': self.query}
            
            # Print findings
            print("\n" + "!"*30 + " ⚠️ ANTI-PATTERNS & MISCONCEPTIONS ⚠️ " + "!"*30)
            print(result[:1500] + "...")
            print("!" * 90 + "\n")
            
        except Exception as e:
            self.log(f"❌ Audit Failed: {e}", level='ERROR')
            self.state = {'anti_patterns': "No anti-patterns identified.", 'query': self.query}
            
        return data
