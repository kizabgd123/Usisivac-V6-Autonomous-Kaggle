import json
import os

REGISTRY_PATH = os.path.join(os.path.dirname(__file__), '../agent-registry/registry.json')

class RoutingEngine:
    def __init__(self):
        with open(REGISTRY_PATH, 'r') as f:
            self.registry = json.load(f)["agents"]
            
    def route_issue(self, issue_category, complexity_score=0):
        """
        Routes the issue to the appropriate agent.
        Security issues or high entropy -> Ollama (local, $0)
        Low complexity -> Ollama
        High complexity -> Gemini / Codex
        """
        if issue_category == "security":
            return self._find_agent("ollama-local")
            
        if complexity_score > 7:
            # Complex task
            return self._find_agent("gemini-cli")
            
        return self._find_agent("ollama-local")
        
    def _find_agent(self, agent_id):
        for agent in self.registry:
            if agent["id"] == agent_id:
                return agent
        return None

if __name__ == "__main__":
    engine = RoutingEngine()
    print("Testing Routing Engine...")
    print("Routing security issue:", engine.route_issue("security")["name"])
    print("Routing complex feature (score 9):", engine.route_issue("feature", 9)["name"])
    print("Routing simple bug (score 3):", engine.route_issue("bug", 3)["name"])
