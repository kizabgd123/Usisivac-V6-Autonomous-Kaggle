import json
import os
from datetime import datetime
from pathlib import Path

class LearningDataStore:
    def __init__(self, storage_dir="data"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
        self.metrics_file = self.storage_dir / "retrospective_metrics.jsonl"
        self.routing_weights_file = self.storage_dir / "routing_weights.json"
        self._init_weights()

    def _init_weights(self):
        if not self.routing_weights_file.exists():
            default_weights = {
                "ollama": 1.0,
                "gemini": 1.0,
                "codex": 1.0,
                "kiro": 1.0
            }
            with open(self.routing_weights_file, "w") as f:
                json.dump(default_weights, f, indent=2)

    def log_task_outcome(self, agent_id: str, issue_type: str, resolution_time_sec: float, quality_score: float, cost: float):
        """
        Metrics schema as defined by NLM:
        agent, issue type, resolution time, quality score, cost
        """
        record = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "agent": agent_id,
            "issue_type": issue_type,
            "resolution_time": resolution_time_sec,
            "quality_score": quality_score,  # 0.0 to 1.0
            "cost": cost
        }
        
        with open(self.metrics_file, "a") as f:
            f.write(json.dumps(record) + "\n")
            
        self._update_feedback_loop(agent_id, quality_score)

    def _update_feedback_loop(self, agent_id: str, quality_score: float):
        """
        Feedback loop that updates routing weights from historical performance.
        Higher quality score increases the weight.
        """
        with open(self.routing_weights_file, "r") as f:
            weights = json.load(f)
            
        current_weight = weights.get(agent_id, 1.0)
        
        # Simple adjustment logic: 
        # If quality > 0.8, increase weight. If < 0.5, decrease weight.
        if quality_score > 0.8:
            new_weight = min(2.0, current_weight * 1.05)
        elif quality_score < 0.5:
            new_weight = max(0.1, current_weight * 0.90)
        else:
            new_weight = current_weight
            
        weights[agent_id] = round(new_weight, 4)
        
        with open(self.routing_weights_file, "w") as f:
            json.dump(weights, f, indent=2)

if __name__ == "__main__":
    store = LearningDataStore()
    # Example usage:
    store.log_task_outcome("ollama", "bug", 120.5, 0.95, 0.0)
    store.log_task_outcome("gemini", "feature", 45.2, 0.40, 0.02)
