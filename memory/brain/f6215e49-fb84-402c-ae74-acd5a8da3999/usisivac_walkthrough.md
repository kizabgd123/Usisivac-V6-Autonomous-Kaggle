# 🏛️ Usisivac — Setup Walkthrough

## Šta je Usisivac?

**ResearchProAI** RAG sistem — pretvara bilo koji projekat u pretraživi vector store koji možeš da upituješ prirodnim jezikom putem Groq/Llama-3.3.

## Instalacija ✅

| Korak | Status | Detalji |
|:---|:---:|:---|
| Git clone | ✅ | `/home/kizabgd/Desktop/kaggle-arena/Usisivac` |
| Dependencies | ✅ | Sve već instalirane (ChromaDB 1.1.1, SentenceTransformers 5.2.2, Groq 0.37.1) |
| `.env` kreiran | ✅ | Kopiran iz `.env.example` — dodaj `GROQ_API_KEY` |
| Ingestovanje | ✅ | **133 fajla → 1172 chunks → ChromaDB** |
| RAG verifikacija | ✅ | Upiti rade, semantic search funkcioniše |

## Struktura

```
Usisivac/
├── src/ingest.py          # Skeniraj dir → ChromaDB  (✅ pokrenuto)
├── src/audit_ingest.py    # Ingestuj WORK_LOG/GUARD_LOG
├── src/generate_report.py # RAG → Groq → Markdown izveštaj
├── src/dashboard.py       # Live CLI prikaz DB stanja
├── chroma_db/             # Vector store (kreiran, 1172 items)
└── .env                   # Dodati GROQ_API_KEY!
```

## Kako koristiti

### 1. Dodaj Groq API ključ
```bash
# Besplatan ključ: https://console.groq.com/
nano /home/kizabgd/Desktop/kaggle-arena/Usisivac/.env
# GROQ_API_KEY=gsk_...
```

### 2. Postavi pitanje o projektu
```bash
cd /home/kizabgd/Desktop/kaggle-arena/Usisivac
python src/generate_report.py "Koji ensemble modeli se koriste u Trinity Protocol?"
python src/generate_report.py "Objasni Guardian validaciju i 7-Gate submit protokol"
python src/generate_report.py "Kako funkcioniše feature engineering u bidding competition?"
```

### 3. Prati stanje DB-a
```bash
python src/dashboard.py
```

### 4. Re-ingestuj (kad dodaš nove fajlove)
```bash
python src/ingest.py /home/kizabgd/Desktop/kaggle-arena
```

### 5. Ingestuj agent logove posebno
```bash
python src/audit_ingest.py
```

## Verifikacija RAG upita

Test upit: *"Trinity Protocol ensemble model"*

```
✅ Result 1: GEMINI.md — Trinity Protocol Ecosystem Constitution v4.0
✅ Result 2: GEMINI.md — Opis metodologije (ansambl modeli, iterativni razvoj)
✅ Result 3: scripts/math/aimo_agent_profiles.py — Trinity 3-6-2 Dialectic Protocol
```

**Semantic search radi ispravno.**

## Napomene

- `chroma_db/` je gitignored — lokalni persistent store
- Embedding model: `all-MiniLM-L6-v2` (lokalno, bez API poziva)
- LLM za izveštaje: Groq Llama-3.3-70b (besplatni tier)
- Samo `.py`, `.json`, `.md`, `.txt`, `.csv`, `.yml` fajlovi se ingestuju
