import os
import sys
import json
import pandas as pd

# Ensure project root is in path
sys.path.append(os.getcwd())

from Usisivac.src.agents.base import MultiAgentOrchestrator
from Usisivac.src.agents.judge_agent import JudgeAgent
from Usisivac.src.agents.usisivac2_agent import Usisivac2Agent

def test_trinity_consensus():
    print("🚀 TESTING TRINITY RULE #2: Multi-Agent Consensus")
    print("-" * 50)
    
    orchestrator = MultiAgentOrchestrator()
    
    # 1. Register V2 Audit (Groq-based)
    orchestrator.register(Usisivac2Agent(query="Audit the proposed portfolio optimization for zoranstojanovic.link"))
    
    # 2. Register Judge (Gemini-based audit)
    orchestrator.register(JudgeAgent())
    
    # 3. Mock mission context
    orchestrator._history.append({
        "agent": "PortfolioAgent",
        "action": "Optimize Portfolio",
        "result": "Added glassmorphism, dynamic gradients, and Inter font. Optimized for SEO."
    })
    
    print("📋 Running Audits...")
    orchestrator.run_pipeline(None)
    
    print("\n✅ Verification complete. Check memory/logs/strategy_audit.jsonl for consensus proof.")

if __name__ == "__main__":
    test_trinity_consensus()
