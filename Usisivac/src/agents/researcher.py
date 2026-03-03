import os
import subprocess
from Usisivac.src.agents.base import BaseAgent

class ResearchAgent(BaseAgent):
    """Bridge agent that uses the existing Usisivac RAG to gather domain knowledge."""
    
    def __init__(self, query: str = "What are the best practices for Telco Churn prediction?"):
        super().__init__('ResearchAgent', 'researcher')
        self.query = query

    def run(self, data, context: dict = None) -> dict:
        self.log(f"🔎 Initiating Research for: '{self.query}'...")
        
        # Call the existing Usisivac generate_report.py
        # We'll use subprocess to simulate a call if we don't want to import the logic directly
        # and because it generates a nice markdown output.
        try:
            cmd = f"python3 Usisivac/src/generate_report.py '{self.query}'"
            result = subprocess.check_output(cmd, shell=True, text=True)
            self.log("✅ Research Complete. Knowledge Base accessed.")
            
            # Store research findings in state
            self.state = {'findings': result, 'query': self.query}
            
            # Print a snippet of findings
            print("\n" + "-"*30 + " RESEARCH FINDINGS " + "-"*30)
            print(result[:1000] + "...")
            print("-" * 79 + "\n")
            
        except Exception as e:
            self.log(f"❌ Research Failed: {e}", level='ERROR')
            self.state = {'findings': "No research available.", 'query': self.query}
            
        return data
