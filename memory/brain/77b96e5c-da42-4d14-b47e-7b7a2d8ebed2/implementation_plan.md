# AIMO 2026 Trinity Solver Implementation Plan

Ovaj plan definiše tehničku implementaciju **AIMO 2026 Trinity Solver-a** zasnovanog na upravo registrovanom **AIMO Strategy Bible** protokolu.

## 🚀 Cilj
Izgradnja autonomnog sistema za rešavanje IMO-nivo matematičkih problema koristeći dialektički pristup (Teza, Antiteza, Sinteza) i ansambl od 5 različitih strategija.

---

## 🏗️ Predložene Promene

### [AIMO Engine]

#### [NEW] [aimo_trinity_solver.py](file:///home/kizabgd/Desktop/kaggle-arena/scripts/math/aimo_trinity_solver.py)
Glavni orkestrator koji implementira:
- **Trinity 3-6-2 Dialectic**: Poziva `Codestral` (Strateg), `Mistral-Large` (Kritičar) i `Gemini 2.0` (Nadzornik).
- **5-Way Voting**: Paralelno (ili sekvencijalno) izvršava `symbolic`, `brute-force`, `hybrid`, `alternative` i `creative` runde.
- **Answer Extraction**: `answer % 100000` logika.
- **D1-D6 Validation**: Integrisani checks za SymPy, edge cases i resurse.

#### [NEW] [aimo_agent_profiles.py](file:///home/kizabgd/Desktop/kaggle-arena/scripts/math/aimo_agent_profiles.py)
Definicija system promptova i parametara za Codestral, Mistral i Gemini modele prema specifikaciji iz Biblije.

---

## 🧪 Plan Verifikacije

### Automatski Testovi
1. **Smoke Test**: Rešavanje jednostavnog problema tipa *"n^2 + 1 deljivo sa 5 za n <= 100"*.
2. **Dimension Check (D1-D6)**: Verifikacija da sintetizovani kod sadrži `try/except` i SymPy imports.
3. **Voting Test**: Simulacija 5 odgovora i provera ispravnosti većinskog glasanja.

### Manuelna Verifikacija
- Provera logova u `GUARD_LOG.md` tokom debate.
- Poređenje rezultata sa `reference.csv`.
