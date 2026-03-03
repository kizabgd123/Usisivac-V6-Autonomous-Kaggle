# 🚢 Usisivac V6: Autonomous Multi-Agent Intelligence System

> **"Usisivač" koji ne samo da prikuplja znanje, već ga pretvara u produkcioni kod.**

## 🏛️ Vizija i Misija
Usisivac V6 je vrhunac autonomije u okviru Trinity Protocol ekosistema. Dok su prethodne verzije bile statični alati, **V6 je živi multi-agent sistem** dizajniran za takmičarsko mašinsko učenje (Kaggle) i kompleksne data science izazove. 

Ovaj sistem je **potpuno reproduktivan** — može se primeniti na bilo koji problem jednostavnim "hranjenjem" baze znanja novim rešenjima.

---

## 🤖 Multi-Agent Arhitektura
Sistem se sastoji od specijalizovanih agenata koji sarađuju putem centralnog **Orchestrator-a**:

1.  **🔎 ResearchAgent**: Inteligentno pretražuje ChromaDB bazu znanja. Izvlači "Golden Recipe" (najbolje prakse) specifične za dati domen.
2.  **🛡️ CriticAgent**: Čuvar kvaliteta. Identifikuje zablude, anti-patterne i zamke koje mogu dovesti do overfitting-a ili curenja podataka.
3.  **🤖 CoderAgent (V6)**: **Mozak operacije.** Na osnovu izveštaja prethodnih agenata, on samostalno piše Python kod (`generated_features.py`).
4.  **🧹 CleanerAgent**: Automatski primenjuje statističko čišćenje, rešava outliere (z-score) i normalizuje podatke.
5.  **⚙️ FeatureAgent (V6)**: Dinamički izvršava kod koji je CoderAgent napisao, transformišući sirove podatke u visoko-performansne feature-e.

---

## 🔑 Ključne Tehnologije i Otpornost
- **RAG (Retrieval-Augmented Generation)**: Koristi ChromaDB i SentenceTransformers za dubinsko razumevanje domena.
- **Key Rotation Protocol**: Implementirana automatska rotacija kroz 5 Gemini API ključeva kako bi se izbegao *Rate Limit (429)*.
- **Mistral Fallback**: Ako Gemini ključevi dostignu kvotu, sistem automatski prelazi na **Mistral (Pixtral-Large)** kao vrhovni autoritet.
- **Rank Blending**: Napredna tehnika stabilizacije ansambla koja garantuje bolji Leaderboard (LB) score.

---

## 🛠️ Kako koristiti Usisivac V6 (Reprodukcija)

### 1. Inicijalizacija Znanja
Postavi sve `.ipynb` (kao tekst), `.py` ili `.txt` fajlove sa rešenjima sličnih problema u `Usisivac/knowledge_base/`. Zatim pokreni:
```bash
python3 Usisivac/src/ingest.py Usisivac/knowledge_base/
```

### 2. Konfiguracija
Kopiraj `.env.example` u `.env` i dodaj svoje API ključeve. Sistem će sam raditi rotaciju.

### 3. Pokretanje Pipeline-a
```bash
make usisivac-v5
```
*Napomena: Komanda `usisivac-v5` pokreće V6 orkestrator (očuvan alias radi kompatibilnosti sa Makefile-om).*

---

## 🧠 Memory Restoration (Gemini Cli)
Ovaj repozitorijum sadrži folder `memory/` koji čuva tvoju "digitalnu svest":
- `/brain`: Prethodne odluke i konteksti.
- `/rules`: Protokoli rada.
- `/skills`: Specijalizovane veštine.

Kada pokrećeš sistem na novoj mašini, isprati uputstvo u `IDE_STARTUP_GUIDE.md` kako bi "ubrizgao" pamćenje nazad u sistem.

---
**Status**: `MASTER_DIRECTIVE_APPROVED`
**Author**: Antigravity Agent (Usisivac Node)
**Source of Truth**: Leaderboard (LB)
