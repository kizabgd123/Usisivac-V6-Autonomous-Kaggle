import os
import time
import json
import re
from datetime import datetime
import pandas as pd
import numpy as np
import chromadb
from chromadb.utils import embedding_functions
from Usisivac.src.skill_registry import SkillRegistry

class BaseAgent:
    """Base class for all Usisivac agents."""
    
    COLORS = {
        'profiler': '🔍',
        'cleaner':  '🧹',
        'eda':      '📊',
        'ml':       '🤖',
        'reporter': '📝',
        'researcher':'🔎',
        'guardian': '🛡️',
        'default':  '⚙️',
    }

    def __init__(self, name: str, role: str):
        self.name  = name
        self.role  = role
        self.logs  = []
        self.state = {}
        self.icon  = self.COLORS.get(role, self.COLORS['default'])

    def log(self, message: str, level: str = 'INFO'):
        ts = datetime.now().strftime('%H:%M:%S')
        log_msg = f"[{ts}] [{self.icon} {self.name}] [{level}] {message}"
        self.logs.append(log_msg)
        print(log_msg)

    def run(self, data, context: dict = None):
        raise NotImplementedError

class MultiAgentOrchestrator:
    """Manages the pipeline execution of multiple agents."""
    
    def __init__(self, workspace_path: str = "."):
        self.agents   = {}
        self.context  = {}
        self.pipeline = []
        self._history = []
        self.workspace_path = workspace_path
        self.skill_registry = SkillRegistry(os.path.join(workspace_path, "memory/skills"))

    def load_skills(self):
        """Populates the context with available skills."""
        skills = self.skill_registry.refresh()
        self.context['available_skills'] = self.skill_registry.get_skill_menu()
        print(f"🧠 Loaded {len(skills)} skills into orchestrator context.")

    def get_best_skill(self, query: str):
        """Finds the most relevant skill using semantic search in ChromaDB."""
        try:
            client = chromadb.PersistentClient(path="chroma_db")
            ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
            collection = client.get_or_create_collection(name="knowledge_base", embedding_function=ef)
            
            results = collection.query(
                query_texts=[query],
                n_results=1,
                where={"type": "skill"}
            )
            
            if results['documents'] and results['documents'][0]:
                skill_name = results['metadatas'][0][0]['name']
                print(f"🎯 Best Skill Found: {skill_name} (Confidence: {1 - results['distances'][0][0]:.2f})")
                return self.skill_registry.skills.get(skill_name)
        except Exception as e:
            print(f"⚠️ Error during skill lookup: {e}")
        return None

    def log_to_memory(self, agent_name: str, activity: str, insight: str = None):
        """Trinity Rule 3: Log strategy extractions to persistent memory."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "agent": agent_name,
            "activity": activity,
            "insight": insight
        }
        # In a real scenario, this would go to Notion/SQLite. 
        # For now, we append to a local JSONL log in memory/
        log_dir = os.path.join(self.workspace_path, "memory/logs")
        os.makedirs(log_dir, exist_ok=True)
        with open(os.path.join(log_dir, "strategy_audit.jsonl"), "a") as f:
            f.write(json.dumps(log_entry) + "\n")

    def register(self, agent: BaseAgent):
        self.agents[agent.name] = agent
        self.pipeline.append(agent.name)
        print(f"✅ Registered Agent: {agent.icon} {agent.name}")

    def run_pipeline(self, data):
        print("\n" + "="*50)
        print(f"🚀 USISIVAC PIPELINE EXECUTION STARTED at {datetime.now().strftime('%H:%M:%S')}")
        self.load_skills() # Dynamic skill injection
        print("="*50 + "\n")

        current = data
        for name in self.pipeline:
            agent   = self.agents[name]
            t0      = time.time()
            try:
                self.context['orchestrator'] = self
                result  = agent.run(current, self.context)
                elapsed = time.time() - t0
                if result is not None:
                    current = result
                self.context[name] = agent.state
                self._history.append({'agent': name, 'icon': agent.icon, 'elapsed': round(elapsed, 2), 'status': 'SUCCESS'})
            except Exception as e:
                elapsed = time.time() - t0
                print(f"❌ Error in Agent {agent.icon} {name}: {e}")
                self._history.append({'agent': name, 'icon': agent.icon, 'elapsed': round(elapsed, 2), 'status': 'FAILED', 'error': str(e)})

        self._summary()
        return current

    def _summary(self):
        print("\n" + "="*50)
        print("📋 USISIVAC PIPELINE SUMMARY")
        print("="*50)
        for h in self._history:
            status = h.get('status', 'SUCCESS')
            status_icon = "✅" if status == 'SUCCESS' else "❌"
            elapsed = h.get('elapsed', 0.0)
            icon = h.get('icon', '🔹')
            agent_name = h.get('agent', 'Unknown')
            print(f"{status_icon} {icon} {agent_name:<25} | {elapsed:>6}s | {status}")
        print("="*50 + "\n")
