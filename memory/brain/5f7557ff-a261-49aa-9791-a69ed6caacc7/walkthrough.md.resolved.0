# Walkthrough: Kaggle Notebooks & Fine-Tuning Pipeline

## Šta je urađeno

### Notebook 1 — [Trinity Multi-Agent Architecture Plan](https://www.kaggle.com/code/kiza123123/trinity-multi-agent-architecture-plan)
Kompletna referenca za multi-agent sistem:
- 4 agent konfiguracije (Research, ML Engine, Kaggle Master, Orchestrator)
- System promptovi za svakog agenta (iz GEMINI.md)
- MCP server šablon (copy-paste za nove agente)
- Mandatory Consultation Protocol dijagram
- Lokalna primena uputstva

### Notebook 2 — [Trinity Fine-Tune Pipeline](https://www.kaggle.com/kiza123123/trinity-fine-tune-pipeline-4-agent-qlora)
QLoRA fine-tuning za sva 4 agenta:
- **80+ trening primera** (10 zajedničkih + domenska za svakog agenta)
- Unsloth/QLoRA na Mistral-7B-Instruct (T4 GPU, ~45 min za sve)
- Push adaptera na HuggingFace Hub
- Inference script za lokalno korišćenje
- MCP server primer sa lokalnim modelom

## Kreirani fajlovi na disku

| Fajl | Opis |
|------|------|
| [trinity-multi-agent-plan.py](file:///home/kizabgd/Desktop/Istrazivanje/kaggle_notebooks/trinity-architecture-plan/trinity-multi-agent-plan.py) | Notebook 1 — Plan |
| [trinity-finetune-pipeline.py](file:///home/kizabgd/Desktop/Istrazivanje/kaggle_notebooks/trinity-finetune-pipeline/trinity-finetune-pipeline.py) | Notebook 2 — Fine-tuning |

## Kako koristiti

### Za fine-tuning (na Kaggle):
1. Otvori [Notebook 2](https://www.kaggle.com/kiza123123/trinity-fine-tune-pipeline-4-agent-qlora)
2. Settings → Accelerator → **GPU T4 × 2**
3. Dodaj `HF_TOKEN` u Kaggle Secrets
4. Pokreni sve ćelije

### Za lokalno korišćenje:
```bash
# Preuzmi adaptere sa HuggingFace (posle treninga)
git clone https://huggingface.co/kiza123123/trinity-guardian-adapter trinity_adapters/guardian_adapter

# Testiraj
python scripts/trinity_inference.py --agent guardian --prompt "Da li da koristim stacking?"
```
