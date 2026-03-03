# Plan: Bidding Predictions for Construction (S6E2) — Thesis Phase (v1.0)

Ovaj plan fokusira se na uspostavljanje baseline-a za Bidding Predictions regresioni problem koristeći Trinity Protokol (3-6-2).

## Proposed Changes

### [ML Engine: Bidding Edition]

#### [NEW] [bidding_factory.py](file:///home/kizabgd/Desktop/kaggle-arena/scripts/bidding_factory.py)
Modul koji transformiše transakcione (item-level) podatke u Job-Contractor profil. Implementira agregacije:
- Sumarna vrednost bidova po paru JOB-CON.
- Statistika količina i broja stavki.

#### [NEW] [thesis_baseline.py](file:///home/kizabgd/Desktop/kaggle-arena/scripts/thesis_baseline.py)
Inicijalna trening skripta:
- Target: `total_bid` (Log-transformed RMSE).
- Model: CatBoostRegressor sa bazičnim parametrima.
- Validacija: 5-Fold Cross-Validation.

#### [MODIFY] [trinity_config.json](file:///home/kizabgd/Desktop/kaggle-arena/trinity_config.json)
Reset metričkih pragova i prelazak na regresione metrike (RMSE).

## Verification Plan

### Automated Tests
1. **JudgeGuard 7-Gate**: Verifikacija da `sample_submission.csv` format odgovara Bidding specifikaciji (row_id, total_bid).
2. **CV Alignment**: Provera da li model konvergira (RMSE < mean baseline).

### Manual Verification
1. **Domen Audit**: Provera da li agregirani bidovi odgovaraju sumama u `train_summary.csv`.
