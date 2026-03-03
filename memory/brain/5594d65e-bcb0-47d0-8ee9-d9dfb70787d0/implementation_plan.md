# Plan: Arize AI Tracing za Trinity Layer

Ovaj plan integriše Arize Phoenix i OpenTelemetry u "Bidding" i "Heart Disease" skripte radi napredne ML opservabilnosti.

## Proposed Changes

### [Bidding & Heart Disease]
#### [MODIFY] [bidding_v14_trinity_fix.py](file:///home/kizabgd/Desktop/Istrazivanje/construction_bidding/bidding_v14_trinity_fix.py)
#### [MODIFY] [heart_v6_final_combined.py](file:///home/kizabgd/Desktop/Istrazivanje/heart_v6_final_combined.py)
- **OpenTelemetry Instrumentation:** Dodavanje `@tracer.start_as_current_span` dekoratora na ključne funkcije (`load_data`, `train_phase`, `apply_priors`).
- **Arize Logging:** Slanje OOF predikcija i feature importance podataka na Arize platformu koristeći `arize.pandas.logger.Client`.

### [Trinity Harvester]
#### [NEW] trinity_tracing_demo.py
- Skripta koja demonstrira kako se koristi Arize za praćenje **Trinity Boardroom** sesija (KIMI, QWEN, MISTRAL).
- Svaka "odluka" agenta u boardroom-u se loguje kao Span.

## Verification Plan
1. **Local Phoenix:** Pokretanje `px.launch()` i provera UI-ja.
2. **Schema Validation:** Provera da li Arize prihvata CatBoost/LGBM DataFrame format bez grešaka.
