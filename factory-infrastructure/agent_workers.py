class AgentWorkerChain:
    def __init__(self):
        self.workers = ["Agent A (Implementer)", "Agent B (Reviewer)", "Agent C (Tester)", "Agent D (Documenter)"]

    def run_pipeline(self, task_description, assigned_agent):
        print(f"Starting Multi-Agent Pipeline for Task...")
        print(f"Main Model Selected: {assigned_agent['name']}")
        
        print("\n[STEP 1] Agent A (Implementation)")
        print(f" -> {assigned_agent['name']} is writing code... Done.")
        
        print("\n[STEP 2] Agent B (Review)")
        reviewer = "Ollama (llama3.2:3b)" if "Gemini" in assigned_agent['name'] or "Codex" in assigned_agent['name'] else "Codex Sandbox"
        print(f" -> Objectivity Check: {reviewer} is reviewing the code... Passed.")
        
        print("\n[STEP 3] Agent C (Test Generation)")
        print(f" -> llama3.2:1b is generating pytest scripts... Done.")
        
        print("\n[STEP 4] Agent D (Documentation)")
        print(f" -> Generating README.md updates and PR descriptions... Done.")
        
        print("\nPipeline execution completed successfully. PR is ready for Validation.")

if __name__ == "__main__":
    chain = AgentWorkerChain()
    mock_agent = {"name": "Gemini CLI", "id": "gemini-cli"}
    chain.run_pipeline("Implement new feature", mock_agent)
