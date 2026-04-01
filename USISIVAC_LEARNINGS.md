# Usisivac V6 Integration Learnings

## 1. Knowledge Inhalation Protocol
The system uses `inhale_github.py` to pull external expertise into the local environment. Adding new tools (like `bolt.new`) requires updating the `REPOSITORIES` dictionary and running the inhalation script followed by `ingest.py`.

## 2. Mistral SDK Versioning
The `mistralai` package (v2.2.0) has moved the main `Mistral` client to `mistralai.client`. Legacy code using `from mistralai import Mistral` must be updated to `from mistralai.client import Mistral`.

## 3. Multi-Agent Consensus (Trinity Rule #2)
The `verify_trinity.py` script is essential for ensuring that specialized agents (Usisivac2Agent, JudgeAgent) can communicate. It relies on the `Usisivac_2` directory structure being present, even if it mirrors the main `Usisivac` logic.

## 4. Bolt.new Integration
Integrated `bolt.new` into the knowledge base to allow the Research and Coder agents to draw from its architecture for web-based AI development patterns.
