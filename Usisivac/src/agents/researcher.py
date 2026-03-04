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
        
        skills = context.get('available_skills', '')
        # Enhance query with context if available
        enhanced_query = self.query
        if skills:
            enhanced_query += f"\n\nContext: You have access to the following skills: {skills}"

        # Call the existing Usisivac generate_report.py
        try:
            cmd = f"python3 Usisivac/src/generate_report.py '{enhanced_query}'"
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
