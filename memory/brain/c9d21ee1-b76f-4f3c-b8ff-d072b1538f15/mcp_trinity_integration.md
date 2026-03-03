# Skaliranje Master Arhitekture: MCP Integracija za Trinity OS

Na osnovu dubinske analize postojećeg radnog okruženja, istorije konverzacija (`.gemini/brain`) i sistemskih ustava (`GEMINI.md`, `trinity_config.json`, `ORCHESTRATION_RULES.json`), cilj je da pređemo sa pasivnog parsiranja konfiguracija na aktivni API-driven LLM pristup putem Model Context Protocol (MCP) standarda.

Ovo će dati našim agentima (AntiGravity OS, Trae) moć kakvu ima JetBrains Junie - **Native IDE execution obogaćen ljudskim Veto checkpoint-ima.**

## 1. Uočeni temelji iz `gemini/brain` radova

Preporučena MCP tranzicija se bazira na tehnologijama koje korisnik već intezivno razvija:
- **Mistral Guardian Fine-Tuning** (Trening Oracle/VetoBoard modela na lokalnim logovima da sprovodi `GEMINI.md`).
- **Notion Syncing** (Baza `data/notion_raw/` koja napaja Sqlite `trinity_kb.db`).
- **Orchestration / JudgeGuard** (`scripts/mistral_guardian.py`, `judge_guard.py` i CLI komande).

## 2. Predlog 4 stacionarna MCP Servera

Da bi se ispoštovala maksimalna Trinity bezbednost (Section §4 Guardrails) i Single Source of Truth pravila, predlažem da **rasparčamo operativne funkcionalnosti u 4 lokalna MCP servera**.

### A. Konfiguracioni Guard (mcp-config-state)
- **Mapiranje**: Enforce-ovanje parametara iz `trinity_config.json` (granice CPU timeout-a, limit za korelacije od 0.95).
- **Zašto MCP**: Agent umesto da sam radi "grep" i pokušava da čita limite, prosto pozove MCP alat: `check_threshold(metric="correlation")`. MCP server mu vraća trenutni state, čime se onemogućava LLM halucinacija limita.

### B. VetoBoard Mistral Oracle (mcp-mistral-vetoboard)
- **Mapiranje**: Section §5 i `Mistral Fine-tuning pipeline`.
- **Kako funkcioniše**: Poput Junie koja pauzira kod terminalskih komandi, pre nego što `Synthesis_Ensembler` uradi `make submit`, on šalje plan akcije MCP VetoBoard-u: `evaluate_action("Apply tabnet + gbdt with UCI prior")`.
- **Backend MCP-a**: Server poziva lokalni Mistral model koji ocenjuje plan prema pravilima. Ako dobije **VETO**, MCP odbija zahtev agenta i agent *mora* da primeni `actionable_fallback` iz loga, što drastično ubrzava učenje.

### C. Knowledge Base RAG (mcp-trinity-kb)
- **Mapiranje**: Sinkronizacija sa Notion-om (`trinity_kb.db`) i `tactic_registries/*.md`.
- **Kako funkcioniše**: Umesto da RAG agent samo baca tekst u prompt, MCP server mu izlaže specifične alate: `fetch_competition_golden_recipe(competition_name="playground-s6e2")`. Server pokreće direktan SQL upit nad SQLite bazom i vraća samo suštinu (npr. pravilo 38 - Tanaka HR formula).

### D. Pipeline & Execution Guard (mcp-judge-guard)
- **Mapiranje**: `judge_guard.py`, 7-Gate Submit protokol, i `Makefile`.
- **Kako funkcioniše**: Agent dobija alat `run_pipeline(task="submit")`. Server na backend-u izvršava kod pod strogim uslovima (validira ekstenzije fajlova, dtype `float64`, inf/nan ček).
- **Efekat Junie Autonomije**: Greške iz terminala se parsiraju i vraćaju nazad u MCP response kao strukturirani JSON. Agent trenutno vidi gde je pogrešio bez da izlazi iz svog toka misli (`chain-of-thought`).

## 3. Tehnička Implementacija i Sledeći Korak
Ovakav sistem pretvara tekstualna (ljudska) pravila u pravila na API novu koja sistem može programski da nadzire. Agent prelazi sa **"mislim da pratim ustav"** na **"procesor mi nije dao pristup alatu jer sam prekršio uslov ustava"**.

**Action Plan:**
1. Trenutni implementacioni plan opisuje ovo arhitekturalno stanje.
2. Ako se odobri, prvi korak je kreiranje `.mcp/` direktorijuma i inicijalizacija (Python based) MCP SDK infrastrukture, počevši sa `mcp-mistral-vetoboard` serverom.
