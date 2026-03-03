import pandas as pd
import os
import sys

# Ensure project root is in path for imports
sys.path.append(os.getcwd())

from Usisivac.src.agents.base import MultiAgentOrchestrator
from Usisivac.src.agents.researcher import ResearchAgent
from Usisivac.src.agents.cleaner import CleanerAgent
from Usisivac.src.agents.feature_agent_v6 import FeatureAgentV6
from Usisivac.src.agents.critic import CriticAgent
from Usisivac.src.agents.coder_v6 import CoderAgentV6

def run_usisivac_v6():
    """Run the Autonomous Multi-Agent Usisivac V6 pipeline."""
    
    print("🚢 USISIVAC V6: Autonomous Multi-Agent Intelligence")
    print("-" * 50)
    
    # 1. Initialize Orchestrator
    orchestrator = MultiAgentOrchestrator()
    
    # 2. Register Agents in Order
    # - ResearchAgent: Gets domain knowledge
    # - CriticAgent: Audits anti-patterns
    # - CoderAgentV6: WRITES code autonomously based on Research & Critic
    # - CleanerAgent: Automates cleaning
    # - FeatureAgentV6: EXECUTES the autonomous code
    
    orchestrator.register(ResearchAgent(query="Best features for ROC AUC in Kaggle Playground S6E3 Telco Churn"))
    orchestrator.register(CriticAgent(query="What are the biggest mistakes, myths, and anti-patterns in Telco Churn prediction?"))
    orchestrator.register(CoderAgentV6())
    orchestrator.register(CleanerAgent(outlier_z=3.5))
    orchestrator.register(FeatureAgentV6())
    
    # 3. Load Data
    data_path = 'data/train.csv'
    if not os.path.exists(data_path):
        print(f"❌ Error: {data_path} not found.")
        return
        
    print(f"📂 Loading Data: {data_path}...")
    df = pd.read_csv(data_path)
    
    # 4. Run Pipeline
    final_data = orchestrator.run_pipeline(df)
    
    # 5. Output Results
    print(f"✨ Final Dataset Ready for Stacking: {final_data.shape}")
    final_data_path = 'data/train_engineered_v6.csv'
    final_data.to_csv(final_data_path, index=False)
    print(f"✅ Engineered Data saved to: {final_data_path}")

if __name__ == "__main__":
    run_usisivac_v6()
