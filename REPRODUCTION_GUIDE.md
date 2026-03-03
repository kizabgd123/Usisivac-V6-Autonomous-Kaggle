# 🛠️ Reproduction & Challenge Guide: Usisivac V6

Ovaj vodič objašnjava kako pokrenuti Usisivac V6 za bilo koje novo takmičenje ili svrhu.

## 🏃 Brzi Start (Quick Start)

1.  **Priprema Baze Znanja**:
    - Ubaci relevantna rešenja (Kaggle kernels, .txt rešenja) u `Usisivac/knowledge_base/`.
    - Pokreni indeksiranje: `python3 Usisivac/src/ingest.py Usisivac/knowledge_base/`.

2.  **Konfiguracija API-ja**:
    - Kopiraj `.env.example` u `.env`.
    - Popuni što više Gemini ključeva (1-4) i Mistral ključ.

3.  **Pokretanje Autonomnog Pipeline-a**:
    ```bash
    make usisivac-v5  # (Ova komanda pokreće V6 orkestrator)
    ```

## 🧠 Kako sistem radi na novom challange-u?

Kada se pokrene, Usisivač će:
1.  **Istražiti**: Sam će pitati bazu znanja "Koji su najbolji feature-i za [TVOJ PROBLEM]?".
2.  **Identifikovati Greške**: Pitaće "Koje su najveće zablude za [TVOJ PROBLEM]?".
3.  **Napisati Kod**: Na osnovu ta dva odgovora, `CoderAgent` će generisati Python kod u `Usisivac/src/agents/generated_features.py`.
4.  **Izvršiti**: `FeatureAgent` će primeniti taj kod na tvoj `train.csv`.

## 📦 Pakovanje za GitHub (Uputstvo za Gemini CLI)

1.  Inicijalizuj git u novom folderu `usisivac_work_pack`.
2.  Dodaj `.gitignore` (obavezno isključi `.env` i `data/*.csv`).
3.  Commit-uj sve fajlove iz ovog paketa.
4.  Push na novi repo pod nazivom `Usisivac-V6-Autonomous-Kaggle`.

---
*Ready for any challenge. Reproducibility confirmed.*
