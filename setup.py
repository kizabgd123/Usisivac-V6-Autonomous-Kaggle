#!/usr/bin/env python3
import os
import shutil
import subprocess
from pathlib import Path

def run_cmd(cmd):
    print(f"Pokrećem: {cmd}")
    subprocess.run(cmd, shell=True, check=False)

def setup_gemini():
    print("\n--- Setup Gemini / Antigravity (agy) ---")
    # Migracija: gemini -> agy (deprecated od 18.06.2026.)
    # Instaliramo novi agy ili koristimo postojeci.
    if not shutil.which("agy"):
        print("agy nije pronađen, instaliram...")
        run_cmd("npm install -g @google/gemini-cli")
    
    # Konfiguracija
    settings_dir = Path(".gemini")
    settings_dir.mkdir(exist_ok=True)
    with open(settings_dir / "settings.json", "w") as f:
        f.write('{"model": "gemini-3.1-pro", "sandbox": true}')
    print("Gemini konfigurisan.")

def setup_kiro():
    print("\n--- Setup Kiro CLI ---")
    kiro_dir = Path.home() / ".kiro" / "agents"
    kiro_dir.mkdir(parents=True, exist_ok=True)
    # Read-only tools by default
    kiro_config = kiro_dir / "default.json"
    with open(kiro_config, "w") as f:
        f.write('{"permissions": "read-only", "tools": ["view_file", "list_dir"]}')
    print("Kiro CLI konfigurisan (read-only mode).")

def setup_ollama():
    print("\n--- Setup Ollama (Lokalno) ---")
    if shutil.which("ollama"):
        run_cmd("ollama pull llama3.2:3b")
        run_cmd("ollama pull mistral")
        
        modelfile_path = Path("agent-registry/Modelfile.agent")
        if modelfile_path.exists():
            run_cmd("ollama create factory-agent -f agent-registry/Modelfile.agent")
    else:
        print("UPOZORENJE: Ollama nije instalirana na sistemu. Ručno instalirajte.")

def setup_codex():
    print("\n--- Setup Codex ---")
    codex_dir = Path.home() / ".codex" / "rules"
    codex_dir.mkdir(parents=True, exist_ok=True)
    # Sandbox mode: workspace-write
    print("Codex konfiguracija: sandbox=workspace-write, approval-mode=auto")
    # Simuliramo kreiranje default.rules
    rule_file = codex_dir / "default.rules"
    with open(rule_file, "w") as f:
        f.write('# Starlark pravila za Codex\ndefault_sandbox = "workspace-write"\n')

if __name__ == "__main__":
    print("Započinjem čisti setup razvojnog okruženja agenata...")
    setup_gemini()
    setup_kiro()
    setup_ollama()
    setup_codex()
    print("\nSetup uspešno završen!")
