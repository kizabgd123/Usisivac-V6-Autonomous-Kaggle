import os
import sys
import json
import chromadb
from mcp.server.fastmcp import FastMCP

# Ensure project root is in path
sys.path.append(os.getcwd())

from Usisivac.src.agents.base import MultiAgentOrchestrator
from Usisivac.src.orchestrator import run_portfolio_mission, run_usisivac_v6
from Usisivac.src.inhale_github import inhale_github

# Initialize FastMCP server
mcp = FastMCP("Usisivac Elite")

# Initialize Orchestrator
orchestrator = MultiAgentOrchestrator()

@mcp.tool()
def run_mission(mission_type: str, query: str = None) -> str:
    """Executes a full Usisivač V6 mission (e.g., 'portfolio', 'kaggle')."""
    try:
        if mission_type == "portfolio":
            result = run_portfolio_mission(url=query or "https://zoranstojanovic.link")
        elif mission_type == "kaggle":
            result = run_usisivac_v6(query=query or "Kaggle Feature Engineering")
        else:
            return f"❌ Unknown mission type: {mission_type}"
        
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"❌ Mission Error: {str(e)}"

@mcp.tool()
def agent_task(agent_name: str, query: str) -> str:
    """Executes a task using a specific Usisivač agent."""
    from Usisivac.src.agents.researcher import ResearchAgent
    from Usisivac.src.agents.critic import CriticAgent
    from Usisivac.src.agents.judge_agent import JudgeAgent
    from Usisivac.src.agents.usisivac2_agent import Usisivac2Agent
    
    agent_map = {
        "researcher": ResearchAgent,
        "critic": CriticAgent,
        "judge": JudgeAgent,
        "v2_audit": Usisivac2Agent
    }
    
    if agent_name.lower() not in agent_map:
        return f"❌ Unknown agent: {agent_name}. Available: {list(agent_map.keys())}"
    
    try:
        # Since judge doesn't take a query
        if agent_name.lower() == "judge":
            agent = JudgeAgent()
        else:
            agent = agent_map[agent_name.lower()](query=query)
        
        # For granular task, we create a temporary orchestrator
        temp_orch = MultiAgentOrchestrator()
        temp_orch.register(agent)
        temp_orch.run_pipeline(None)
        
        return f"✅ Agent {agent_name} task complete. Insight: check logs."
    except Exception as e:
        return f"❌ Agent Error: {str(e)}"

@mcp.tool()
def find_skill(query: str) -> str:
    """Finds the most relevant autonomous skill via RAG search."""
    skill = orchestrator.get_best_skill(query)
    if skill:
        return json.dumps(skill, indent=2)
    return "No matching skill found."

@mcp.tool()
def inhale_repo() -> str:
    """Triggers the background knowledge 'inhalation' for external GitHub repositories."""
    try:
        inhale_github()
        return "✅ Knowledge inhalation complete. ChromaDB updated."
    except Exception as e:
        return f"❌ Inhale Error: {str(e)}"

@mcp.tool()
def get_audit_logs(limit: int = 10) -> str:
    """Retrieves the latest strategy audit logs (Trinity Rule #3)."""
    log_path = os.path.join(os.getcwd(), "memory/logs/strategy_audit.jsonl")
    if not os.path.exists(log_path):
        return "No audit logs found."
    
    try:
        with open(log_path, "r") as f:
            lines = f.readlines()
            return "".join(lines[-limit:])
    except Exception as e:
        return f"❌ Log Error: {str(e)}"

if __name__ == "__main__":
    mcp.run()
