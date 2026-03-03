# Implementacija Heart Disease Misije - Plan

## Cilj
Organizacija i implementacija end-to-end pipeline-a za predviđanje srčanih oboljenja (Kaggle Playground S6E2) u skladu sa Trinity Protokolom v4.0.

## Strategija (3-6-2 Dialectic)

### Phase 1: Thesis (Baseline)
- [ ] Implementacija `scripts/heart_disease_baseline.py` koristeći CatBoost.
- [ ] Postavljanje robustnog CV (Stratified K-Fold).
- [ ] Generisanje prvog submission-a.

### Phase 2: Antithesis (Diversity)
- [ ] Implementacija `scripts/heart_disease_antithesis.py`.
- [ ] Uvođenje ortogonalnih modela (XGBoost, LightGBM, TabNet).
- [ ] Feature Engineering zasnovan na `tactic_registries/heart_disease.md`.

### Phase 3: Synthesis (Ensemble)
- [ ] Implementacija `scripts/heart_disease_synthesis.py` (Rank-based Blending).
- [ ] Finalni "Killshot" model.

## Tehničke Izmene

### Konfiguracija
- [ ] Ažuriranje `manifest.json` za `playground-series-s6e2`.
- [ ] Postavljanje pragova u `trinity_config.json`.

### Automatizacija
- [ ] Kreiranje `Makefile` targeta za HD misiju.
- [ ] JudgeGuard integracija.

## Verifikacija
- [ ] Lokalni CV vs LB (ako je moguće).
- [ ] Guardian validacija (Gate 1-7).
