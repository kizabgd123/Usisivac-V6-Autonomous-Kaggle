import subprocess
import os

class AgentWorkerChain:
    def _run_cmd(self, cmd):
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            return f"Error: {e.stderr.strip()}"

    def call_model(self, agent_id, prompt):
        """
        Pravo pozivanje AI modela. Koristi Gemini CLI ili Ollama.
        """
        if "gemini" in agent_id.lower():
            return self._run_cmd(f'gemini ask "{prompt}"')
        else:
            return self._run_cmd(f'ollama run llama3.2:3b "{prompt}"')

    def run_pipeline(self, task_description, assigned_agent):
        print(f"Pokrećem PRAVI Multi-Agent Pipeline...")
        agent_id = assigned_agent['id']
        
        print("\n[KORAK 1] Agent A (Programer)")
        print(f" -> Zovem {agent_id} API da generiše kod...")
        code_result = self.call_model(agent_id, f"Write python code for: {task_description}. Return only code without markdown blocks.")
        with open("generated_feature.py", "w") as f:
            f.write(code_result)
        print(" -> Fajl 'generated_feature.py' je kreiran.")
        
        print("\n[KORAK 2] Agent B (Revizor)")
        reviewer_id = "ollama" if "gemini" in agent_id.lower() else "gemini"
        print(f" -> Zovem {reviewer_id} da pregleda kod (Objektivnost)...")
        review = self.call_model(reviewer_id, f"Review this python code and suggest fixes:\n{code_result}")
        with open("review_report.md", "w") as f:
            f.write(review)
        print(" -> Izveštaj o pregledu 'review_report.md' je kreiran.")
        
        print("\n[KORAK 3] Agent C (Tester)")
        print(f" -> Generišem pytest skripte preko {agent_id}...")
        tests = self.call_model(agent_id, f"Write pytest tests for this code:\n{code_result}")
        with open("test_generated.py", "w") as f:
            f.write(tests)
        print(" -> Testovi 'test_generated.py' su kreirani.")
        
        print("\n[KORAK 4] Agent D (Dokumentarista)")
        print(" -> Pravim README i tekst za PR...")
        docs = self.call_model(agent_id, f"Write a Pull Request description for this code implementation:\n{code_result}")
        with open("pr_description.md", "w") as f:
            f.write(docs)
        print(" -> PR opis 'pr_description.md' je kreiran.")
        
        print("\nPipeline završen. Kod je generisan. Prelazim na Validaciju...")

if __name__ == "__main__":
    chain = AgentWorkerChain()
    # Pravi primer
    chain.run_pipeline("Create a function that calculates fibonacci sequence", {"name": "Gemini CLI", "id": "gemini-cli"})
