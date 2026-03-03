import os
import time
import json
import re
from datetime import datetime
import pandas as pd
import numpy as np

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

    def register(self, agent: BaseAgent):
        self.agents[agent.name] = agent
        self.pipeline.append(agent.name)
        print(f"✅ Registered Agent: {agent.icon} {agent.name}")

    def run_pipeline(self, data):
        print("\n" + "="*50)
        print(f"🚀 USISIVAC PIPELINE EXECUTION STARTED at {datetime.now().strftime('%H:%M:%S')}")
        print("="*50 + "\n")

        current = data
        for name in self.pipeline:
            agent   = self.agents[name]
            t0      = time.time()
            try:
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
            status_icon = "✅" if h['status'] == 'SUCCESS' else "❌"
            print(f"{status_icon} {h['icon']} {h['agent']:<25} | {h['elapsed']:>6}s | {h['status']}")
        print("="*50 + "\n")
