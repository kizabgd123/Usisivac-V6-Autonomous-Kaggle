# Configure AI Agent IDE Context Sync for Trinity Protocol

The goal is to configure the `ai-agent-ide-context-sync` extension to support the Trinity protocol, Kaggle competitions, and AIMO problems, according to the user's prompt. We will create the configuration files in `.ai-workspace`.

## Proposed Changes

We will create the following files in the workspace's `.ai-workspace` structure:

### Personas (`.ai-workspace/personas/`)

#### [NEW] `thesis_builder.md`
Zadužen za postavljanje baznog modela i početno učitavanje podataka za Kaggle takmičenja.
Context: `GEMINI.md`, `trinity_config.json`, kod baznog modela, EDA notebook-ovi.

#### [NEW] `antithesis_engineer.md`
Fokusiran na feature engineering, istraživanje različitih modela i generisanje ortogonalnih feature-a za Kaggle.
Context: `GEMINI.md`, `KAGGLE_GRANDMASTER_HARVEST.md`, `trinity_config.json`, skripte za feature engineering.

#### [NEW] `synthesis_ensembler.md`
Kombinuje modele iz Thesis i Antithesis faza, vrši blending i finalnu validaciju za Kaggle.
Context: `GEMINI.md`, skripte za ensembling, `trinity_config.json`, OOF rezultati.

#### [NEW] `kaggle_analyst.md`
Analizira podatke i priprema submission fajlove za Kaggle takmičenja.
Context: `GEMINI.md`, podaci za Kaggle takmičenje, `trinity_config.json`.

#### [NEW] `strateg_aimo.md`
Generiše početni kod i strategije za AIMO probleme prema `AIMO_Strategy_Bible.md`.
Context: `AIMO_Strategy_Bible.md`, opis problema, `trinity_config.json`.

#### [NEW] `kriticar_aimo.md`
Vrednuje i proverava kod generisan od strane Strateg_AIMO, pronalazi greške prema dimenzijama validacije.
Context: `AIMO_Strategy_Bible.md`, kod od Strateg-a, `GEMINI.md`.

#### [NEW] `nadzornik_aimo.md`
Sintetiše konačna rešenja i kod za AIMO probleme.
Context: `AIMO_Strategy_Bible.md`, `GEMINI.md`, `trinity_config.json`.

---

### Tasks (`.ai-workspace/tasks/`)

#### [NEW] `kaggle_spaceship_titanic.md`
Board/projekat: "Spaceship Titanic Competition"
Glavni zadatak: "Implementacija V15.6 Upgrade" (Faza: Synthesis)
Pod-zadaci:
- "Faza 1: Free Wins - Implement Rank Transformation" (Persona: Antithesis_Engineer)
- "Faza 2: Arhitektura - Implement Hill Climbing" (Persona: Antithesis_Engineer)
- "Faza 3: Blending - Optimizacija Težina" (Persona: Synthesis_Ensembler)

#### [NEW] `aimo_problem_123.md`
Board/projekat: "AIMO Problem 123"
Glavni zadatak: "Rešavanje AIMO problema 123"
Pod-zadaci:
- "Run 1: Simboličko takmičenje" (Persona: Strateg_AIMO) -> Pod-zadaci: "Strateg: Generiši kod", "Kritičar: Proveri kod", "Nadzornik: Sintetiši kod"
- "Run 2: Brute-Force takmičenje"

---

### Context Synchronization (`.ai-workspace/rules/`)

We will configure rules to ensure contexts specified above are automatically synced and applied to the corresponding personas and tasks.

#### [NEW] `context_sync_rules.md`
Context rules mapping the specific directories and files to Personas and Tasks.

## Verification Plan

### Manual Verification
1. User verifies the markdown schemas in `.ai-workspace` are picked up by the `ai-agent-ide-context-sync` extension correctly.
2. The user validates that activating a Kaggle or AIMO task correctly prompts the relevant Persona with its assigned context.
