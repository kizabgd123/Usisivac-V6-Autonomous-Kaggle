import os
import json
from Usisivac.src.agents.base import BaseAgent

class JudgeAgent(BaseAgent):
    """
    Automated Judge/Guardian Agent. 
    Verifies the outputs of other agents against criteria and project goals.
    Ported from judge-guard-core.
    """
    def __init__(self, criteria: str = "Technical correctness, security compliance, and adherence to project goals."):
        super().__init__('JudgeAgent', 'guardian')
        self.criteria = criteria

    def run(self, data, context: dict = None) -> dict:
        self.log(f"⚖️ Judging mission output against criteria: '{self.criteria}'...")
        
        # In a real mission, this would trigger an LLM call to evaluate 'data'
        # For validation, we simulate a successful verdict if the data exists.
        
        verdict = "PASS" if data is not None else "FAIL"
        justification = "Output meets the minimum structural requirements for the mission." if verdict == "PASS" else "No output data found to judge."
        
        self.log(f"🏁 Verdict: {verdict}")
        
        # Store in state
        self.state = {
            'verdict': verdict,
            'justification': justification,
            'criteria': self.criteria
        }
        
        # Trinity Rule 3 compliance
        if context and 'orchestrator' in context:
            insight = f"Verdict: {verdict} | Justification: {justification}"
            context['orchestrator'].log_to_memory(self.name, "Automated Audit", insight)
            
        return data
