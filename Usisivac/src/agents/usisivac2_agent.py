import os
import subprocess
from Usisivac.src.agents.base import BaseAgent

class Usisivac2Agent(BaseAgent):
    """
    The Usisivač 2 (ResearchProAI) Agent.
    Uses the Groq-powered RAG engine from the Usisivac_2 directory.
    """
    def __init__(self, query: str = "Perform a codebase audit."):
        super().__init__('Usisivac2Agent', 'researcher_v2')
        self.query = query

    def run(self, data, context: dict = None) -> dict:
        self.log(f"🔍 Running Usisivač 2 RAG Analysis: '{self.query}'...")
        
        try:
            # We execute the Usisivac_2/src/generate_report.py script directly
            # This ensures we use its specific logic and environment (if different)
            cmd = [
                "python3", 
                "Usisivac_2/src/generate_report.py", 
                self.query
            ]
            result = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)
            self.log("✅ Analysis Complete.")
            
            # Store report in state
            self.state = {
                'report': result,
                'query': self.query
            }
            
            # Trinity Rule 3 compliance
            if context and 'orchestrator' in context:
                context['orchestrator'].log_to_memory(self.name, "RAG V2 Audit", result[:500] + "...")
                
        except Exception as e:
            self.log(f"❌ Error in Usisivač 2: {str(e)}")
            self.state = {'error': str(e)}

        return data
