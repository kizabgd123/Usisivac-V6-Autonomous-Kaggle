# Novi Čist Workspace za Kaggle Takmičenja

## Problem

Trenutni workspace (`/home/kizabgd/Desktop/Istrazivanje`) ima **102 direktorijuma i 104 fajla** — akumuliranih iz 10+ takmičenja i eksperimenata. Teško se snalazi, mnogi fajlovi su zastareli, a okruženje nije optimizovano za novo takmičenje.

## Predlog

Kreirati novi čist workspace na `/home/kizabgd/Desktop/kaggle-arena` sa sljedećom strukturom:

## User Review Required

> [!IMPORTANT]
> **Lokacija novog workspace-a**: Predlažem `/home/kizabgd/Desktop/kaggle-arena`. Da li je ovo OK, ili želiš drugu lokaciju?

> [!IMPORTANT]  
> **Stari workspace**: Stari workspace ostaje netaknut na `/home/kizabgd/Desktop/Istrazivanje` kao arhiva. Ništa neće biti obrisano.

---

## Proposed Changes

### 1. Struktura Novog Workspace-a

```
kaggle-arena/
├── .agent/
│   ├── rules/
│   │   └── ORCHESTRATION_RULES.json     # Očišćen, bez starih competition entries
│   ├── workflows/                       # Samo univerzalni workflow-i (7 od 20)
│   │   ├── DYNAMIC_EFFECTIVENESS_SCORING.md
│   │   ├── PRODUCT_GUARDIAN_PROTOCOL.md
│   │   ├── PROJECT_AUDIT_PROTOCOL.md
│   │   ├── REVENUE_DRIVEN_WORKFLOW.md
│   │   ├── guardian_v2.md
│   │   ├── mistral_trigger.md
│   │   └── trinity_start.md
│   └── skills/
├── .env                                 # Svi API ključevi (preneseni 1:1)
├── .env.example                         # Template bez vrednosti
├── .gitignore
├── GEMINI.md                            # Ustav — prenesen 1:1
├── trinity_config.json                  # Očišćen za novi domen
├── tactic_registries/
│   └── competition_tracker.md           # Prazan tracker za novo takmičenje
├── scripts/
│   └── judge_guard.py                   # Univerzalni JudgeGuard
├── Makefile                             # Čist entry point
├── WORK_LOG.md                          # Prazan
├── GUARD_LOG.md                         # Prazan
└── README.md                            # Kratka dokumentacija
```

### 2. Šta se prenosi (1:1 kopija)

| Fajl | Izvor | Razlog |
|---|---|---|
| `.env` | Stari workspace | Svi API ključevi (13 servisa) |
| `GEMINI.md` | Stari workspace | Projektni ustav (nepromenjeno) |
| `.agent/rules/ORCHESTRATION_RULES.json` | Stari workspace | Očišćen od starih takmičenja |
| `trinity_config.json` | Stari workspace | Resetovan na generičke parametre |
| 7 workflow-a | `.agent/workflows/` | Samo univerzalni (bez heart_disease, melting_point itd.) |

### 3. Šta se čisti iz `ORCHESTRATION_RULES.json`

- **`competition_registry.active`**: Uklanja se S6E2, WiDS, AIMO — prazan za novo takmičenje
- **`competition_registry.completed`**: Čuva se kao istorija
- **`judge_guard_protocol.best_scores`**: Uklanjaju se stari skorovi
- **`intelligence_harvester.path`**: Popravlja se iz "New Folder"

### 4. Šta se čisti iz `trinity_config.json`

- **`domain`**: Resetuje se iz "construction_bidding" → "pending"
- **`thresholds.current_baseline_auc`**: Resetuje se na `null`
- **`structured_params`**: Čiste se heart disease specifični parametri
- **`kb_orchestrator.search_patterns`**: Ažurira se za novi workspace path

### 5. Workflow-i koji se NE prenose (domenski specifični)

Ovi su vezani za prethodna takmičenja/projekte i ne trebaju u novom workspace-u:
- `aimo_solver.md`, `alkohol.md`, `melting_point.md`, `trinity_killshot.md`, `trinity_harvest.md`, `trinity_dashboard.md`, `trinity_mentor.md`, `fast-food-dominion.md`, `smoke_test_hybrid.md`, `unify_product.md`, `aaaaa.md`, itd.

---

## Verification Plan

### Automated Tests
```bash
# 1. Provera da svi API ključevi postoje u novom .env
diff <(grep '=' /home/kizabgd/Desktop/Istrazivanje/.env | sort) \
     <(grep '=' /home/kizabgd/Desktop/kaggle-arena/.env | sort)

# 2. Provera strukture direktorijuma
ls -la /home/kizabgd/Desktop/kaggle-arena/.agent/rules/
ls -la /home/kizabgd/Desktop/kaggle-arena/.agent/workflows/

# 3. JSON validacija
python3 -c "import json; json.load(open('/home/kizabgd/Desktop/kaggle-arena/trinity_config.json'))"
python3 -c "import json; json.load(open('/home/kizabgd/Desktop/kaggle-arena/.agent/rules/ORCHESTRATION_RULES.json'))"

# 4. Kaggle CLI test
cd /home/kizabgd/Desktop/kaggle-arena && kaggle competitions list -s "playground" | head -5
```
