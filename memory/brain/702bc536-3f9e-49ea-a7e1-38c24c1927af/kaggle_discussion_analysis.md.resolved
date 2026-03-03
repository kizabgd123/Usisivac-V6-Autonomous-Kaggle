# 🏆 Kaggle S6E2 — Diskusije vs Naš Pristup (Gap Analiza)

## Leaderboard Kontekst

| Rang | AUC Opseg | Pristup |
|---|---|---|
| Top 1-5% | **0.960 — 0.964** | Full pipeline: TargetEnc + OHE + RFE + Hill Climbing ensemble |
| Top 10% | **0.955 — 0.960** | Dobar ensemble, originalni podaci, bazni FE |
| Top 25% | **0.950 — 0.955** | Jedan model ili slab ensemble bez orig. data |
| **Mi (KillShot v3.2 OOF)** | **~0.955** | LGB+XGB+Cat+ET, Nelder-Mead weights, dedup |

---

## 📊 Uporedna Tabela: Top Rešenja vs Naš v3.2

### ✅ Šta Radimo Ispravno

| Tehnika | Top Rešenja | Naš v3.2 | Status |
|---|---|---|---|
| Originalni UCI podaci | ✅ Kritično | ✅ Merge + dedup | ✅ OK |
| Deduplication | ✅ Diskutovano | ✅ `drop_duplicates()` | ✅ OK |
| MICE Imputation za Chol=0 | ✅ Preporučeno | ✅ `IterativeImputer` | ✅ OK |
| Log transformacija | ✅ Za ST depression | ✅ `np.log1p()` | ✅ OK |
| ExtraTreesClassifier | ✅ Forum preporuka | ✅ 1000 estimatora | ✅ OK |
| 4-model ensemble | ✅ LGB+XGB+Cat+... | ✅ LGB+XGB+Cat+ET | ✅ OK |
| Rank averaging | ✅ Ključno | ✅ Nelder-Mead rank | ✅ OK |
| Adversarial Validation | ✅ Za sanity check | ✅ Implementirano | ✅ OK |

### ❌ Šta Nam Nedostaje (GAPOVI)

| # | Tehnika | Top Score Impact | Naš Status | Prioritet |
|---|---|---|---|---|
| **1** | **Target Encoding (CV)** | 🔴 **HUGE BOOST** — označeno kao "CRITICAL" | ❌ Potpuno nedostaje | **P0** |
| **2** | **Thallium × ChestPain interakcija** | 🔴 Najvažniji engineered feature | ❌ Nedostaje | **P0** |
| **3** | **Health_score feature** | 🔴 Drugi najvažniji feature | ❌ Nedostaje | **P0** |
| **4** | **Agresivna Feature Selekcija (RFE)** | 🟡 Od 97 → 25 features | ❌ Nema selekcije | **P1** |
| **5** | **OHE za pseudo-kategoričke** | 🟡 ChestPain, EKG, Slope → OHE | ❌ Tretiramo kao numeric | **P1** |
| **6** | **Yeo-Johnson transformacija** | 🟡 Normalizacija distribucija | ⚠️ Samo log1p | **P1** |
| **7** | **Hill Climbing ensemble** | 🟡 Automatski pronalazi optimalne weights | ⚠️ Nelder-Mead (slično ali manje robusno) | **P2** |
| **8** | **Pseudo-labeling** | 🟠 Risky ali koristan | ❌ Nedostaje | **P2** |
| **9** | **Multi-seed (3-5)** | 🟡 Smanjuje varijansu | ⚠️ Samo 1 seed | **P2** |
| **10** | **CV_risk_score, Multiple_risks** | 🟡 Klinički relevantni | ❌ Nedostaji | **P2** |

---

## 🔍 Detaljna Analiza Ključnih Gapova

### GAP #1: Target Encoding (CV) — **KRITIČNO** ❗

**Šta kažu diskusije:**
> *"Target encoding is CRITICAL! Huge boost!"*

**Kako radi:**
```python
# Za svaki fold u CV:
for fold in folds:
    train_fold = train[train.fold != fold]
    val_fold = train[train.fold == fold]
    
    for col in ['Chest pain type', 'Thallium', 'Slope of ST', 'EKG results']:
        means = train_fold.groupby(col)['Heart Disease'].mean()
        val_fold[f'{col}_target_enc'] = val_fold[col].map(means)
```

**Zašto je moćno:** Hvata nelinearne odnose između kategoričkih varijabli i targeta. Na primer, `Thallium=7` ima potpuno drugačiju distribuciju Heart Disease od `Thallium=3`.

**Naš propust:** Koristimo raw integer vrednosti za kategoričke feature-e.

---

### GAP #2: Thallium × ChestPain Interakcija — **KRITIČNO** ❗

**Šta kažu diskusije:**
> *"Thallium_ChestPain" i "Health_score" su identifikovani kao DVA NAJVAŽNIJA engineered feature-a od ukupno 97!*

**Top 25 najkorisnijih feature-a (od 97 testiranih):**
1. **Thallium_ChestPain** ← ❌ Nedostaje
2. **Health_score** ← ❌ Nedostaje  
3. Sex_ChestPain ← ❌ Nedostaje
4. Age_Sex ← ❌ Nedostaje
5. MaxHR_ExerciseAngina ← ✅ Imamo (`ExAngina_MaxHR`)
6. ST_Slope ← ✅ Imamo
7. Vessels_Thallium ← ❌ Nedostaje
8. HR_Age_ratio ← ❌ Nedostaje (imamo `Age_MaxHR` ali kao product, ne ratio)
9. ST_HR_ratio ← ❌ Nedostaje
10. Vessels_Age_ratio ← ❌ Nedostaje
11. CV_risk_score ← ❌ Nedostaje
12. Multiple_risks ← ❌ Nedostaje
13-25: Originalni features

**Mi imamo samo 3 od top 12 engineered features!**

---

### GAP #3: OHE za Pseudo-Kategoričke

**Šta kažu diskusije:**
> *"Properly treating numerical columns that are actually categorical (e.g., Chest pain type, EKG results) by using one-hot encoding (OHE) instead of keeping them as numeric can improve generalization."*

Naš v3.2 tretira `Chest pain type` (0-3), `EKG results` (0-2), `Slope of ST` (0-2), `Thallium` (0-3) kao **numeričke** feature-e. Ovo je pogrešno jer:
- `Chest pain type = 2` nije "dvostruko veće" od `type = 1`
- Model dobija lažan signal da postoji ordinalnost gde je nema

---

### GAP #4: "Flipped Labels" — Ključan Insight ⚡

**Šta kažu diskusije:**

> [!IMPORTANT]
> **NE BRIŠITE "flipped" redove!** Uklanjanje noisy podataka može da inflacira CV ali da UBIJE LB score jer test set SADRŽI isti noise.

**Prava strategija:** Model treba da NAUČI da rangira ove teške slučajeve bolje, ne da ih ignoriše. AUC meri relativno rangiranje, tako da čak i ako model nije siguran u "flipped" red, dovoljno je da ga bolje rangira u odnosu na ostale nesigurne.

**Naš status:** Mi ne brišemo flipped labels (dobro!), ali nemamo eksplicitno modelovanje conditional noise-a.

---

## 🎯 Preporučeni Plan za Poboljšanje (od Najvišeg Prioriteta)

### Iteracija 1 — Quick Wins (očekivano: +0.005 AUC → 0.960)
1. **Dodati Target Encoding** za `Chest pain type`, `Thallium`, `Slope of ST`, `EKG results`
2. **Dodati ključne interakcije:** `Thallium_ChestPain`, `Health_score`, `Sex_ChestPain`, `Age_Sex`
3. **Dodati ratio feature-e:** `HR_Age_ratio`, `ST_HR_ratio`, `Vessels_Thallium`, `Vessels_Age_ratio`

### Iteracija 2 — Feature Refinement (očekivano: +0.002 AUC → 0.962)
4. **OHE za pseudo-kategoričke** kolone
5. **Yeo-Johnson** umesto samo log1p
6. **RFE sa CV** za feature selection (od ~35 → top 25)

### Iteracija 3 — Ensemble Enhancement (očekivano: +0.001 AUC → 0.963)
7. **Hill Climbing** za automatsku optimizaciju ensemble weight-a
8. **3 seed-a** umesto 1 (ali i dalje 5 foldova)
9. **Pseudo-labeling** samo high-confidence test predviđanja (>0.98)

---

## ⚡ Zaključak

> [!CAUTION]
> **Naš najveći propust je TARGET ENCODING.** Top diskusije ga eksplicitno označavaju kao "CRITICAL" i "Huge boost". Bez njega, naš ceiling je ~0.955-0.957 OOF. Sa njim, ceiling raste na 0.960-0.964.

**Realni target za KillShot v3.3:**
- Sa Iteracijom 1: **0.958-0.960 OOF** → **0.955+ LB**
- Sa Iteracijama 1+2: **0.960-0.962 OOF** → **0.957+ LB**
- Sa svim 3 iteracijama: **0.962-0.964 OOF** → **0.960+ LB**
