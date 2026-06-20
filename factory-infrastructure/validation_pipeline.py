import subprocess
import sys

class ValidationPipeline:
    def __init__(self):
        # Prave CLI komande koje vrše validaciju
        self.steps = [
            ("Ruff Linting", "ruff check ."),
            ("Gitleaks Secret Scan", "gitleaks detect --no-git --source ."),
            # SonarQube bi zahtevao server, pa ćemo pokrenuti pytest kao treći korak sigurnosti
            ("Pytest Execution", "pytest test_generated.py")
        ]

    def run_validation(self):
        print(f"--- Starting REAL Validation Pipeline ---")
        all_passed = True
        
        for name, cmd in self.steps:
            print(f"Pokrećem {name} ({cmd})...")
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"❌ {name} FAILED!")
                print(result.stdout or result.stderr)
                all_passed = False
            else:
                print(f"✅ {name} PASSED.")
                
        if not all_passed:
            print("🚨 VALIDACIJA PALA! Kod ne sme ići u repozitorijum. Zaustavljam pipeline.")
            sys.exit(1)
            
        print("--- Validacija uspešna. Nema curenja podataka, kod je formatiran. ---")

if __name__ == "__main__":
    pipeline = ValidationPipeline()
    pipeline.run_validation()
