# ☁️ Google Colab Setup Guide (V10.14)

Ovaj kod je **100% kompatibilan** sa Google Colab-om. Prati ove korake za start:

### 1. Priprema Podataka
Preuzmi `train.csv` i `test.csv` sa Kaggle-a i jednostavno ih **drag-n-drop** u Colab panel (sekcija sa folderom levo).
> [!TIP]
> Ako imaš `Heart_disease_statlog.csv`, ubaci i njega za dodatni boost!

### 2. Copy-Paste Kod
Otvori [heart_pipeline_v10_14_sota.py](file:///home/kizabgd/Desktop/Istrazivanje/heart_pipeline_v10_14_sota.py), kopiraj ceo sadržaj i nalepi u prvu ćeliju.

### 3. Instalacija (opciono)
Većina biblioteka je već tu. Ako slučajno fali `catboost`, dodaj ovo na sam vrh:
```python
!pip install -q catboost
```

### 4. Run 🚀
Pritisni `Ctrl + Enter`. Program će sam detektovati podatke, odraditi 10-fold CV i izbaciće ti `submission_v14_sota_...csv`.

---

**Zašto je ovo dobro za Colab?**
- **Memorija**: Optimizovano da ne "pukne" RAM (koristi se `gc.collect()`).
- **Brzina**: Iako koristi 10 foldova, dataset je mali, pa će završiti za par minuta.
- **Auto-Path**: Skripta sama traži fajlove u `/content/` folderu.
