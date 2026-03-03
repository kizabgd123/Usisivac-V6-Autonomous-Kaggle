# 🤖 Gemini CLI Startup Guide: Usisivac V6 Deployment

Ovaj vodič je namenjen tebi, **Gemini CLI**, kako bi mogao da preuzmeš i pokreneš ovaj sistem u bilo kom novom okruženju sa punim kapacitetom "pamćenja" i autonomije.

## 1. Priprema Okruženja (Environment Setup)

Preporučuje se korišćenje Python 3.10+ i virtuelnog okruženja:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

*Napomena: Ako `requirements.txt` nedostaje, instaliraj sledeće:*
`pip install pandas numpy scikit-learn lightgbm catboost chromadb sentence-transformers google-generativeai mistralai python-dotenv scipy`

## 2. Restauracija Memorije (Memory Injection)

Usisivač koristi "globalnu memoriju" kako bi prepoznao tvoj stil rada i prethodne odluke.
Fajlovi u folderu `/memory` treba da budu sinhronizovani sa tvojim lokalnim Gemini CLI sistemom:

- Sadržaj `memory/brain/` kopiraj u svoju lokalnu `antigravity/brain/` putanju.
- Sadržaj `memory/rules/` i `memory/skills/` kopiraj u odgovarajuće foldere.
- `research_data.db` je tvoja baza dosadašnjih istraživanja.

## 3. Konfiguracija Autonomije (.env)

Sistem je spreman za rotaciju ključeva. Kopiraj `.env.example` u `.env` i postavi:
- Bar 2 Gemini ključa (za rotaciju).
- **MISTRAL_API_KEY** (kao "vladara" i finalni fallback).

## 4. Inicijalizacija i "Usisavanje" (Ingestion)

Za svaki novi izazov, prati ove korake:

1.  **Znanje**: Ubaci sve relevantne .ipynb (kao .txt) ili .py fajlove u `Usisivac/knowledge_base/`.
2.  **Indeksiranje**:
    ```bash
    python3 Usisivac/src/ingest.py Usisivac/knowledge_base/
    ```
    Ovo puni ChromaDB i omogućava agentima da "uče" iz primera.

## 5. Pokretanje Autonomnog Ciklusa

Kada su podaci (`data/train.csv`) i znanje spremni, pokreni:

```bash
make usisivac-v5
```

**Šta će se desiti (TVOJA ULOGA):**
1.  **ResearchAgent** će pitati bazu znanja o najboljim praksama.
2.  **CriticAgent** će izvući šta su greške i zablude.
3.  **CoderAgentV6** će sam generisati `Usisivac/src/agents/generated_features.py`.
4.  **FeatureAgentV6** će izvršiti taj kod i pripremiti dataset.

## 6. Github Workflow

Kada završiš jedan krug:
1.  `git add .` (pazi da ne dodaš .env i .csv).
2.  `git commit -m "feat: Autonomous cycle [TIMESTAMP] complete - LB Score: [SCORE]"`
3.  `git push origin main`

---
*Ti si sada vlasnik ovog sistema. Čuvaj memoriju, rotiraj ključeve i pusti Usisivač da reši problem.*
