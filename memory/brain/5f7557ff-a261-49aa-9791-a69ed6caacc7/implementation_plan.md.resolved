# Trinity 4-Agent Fine-Tuning — Implementacioni Plan v2.0

## Cilj
Uspešno trenirati 4 specijalizovana LoRA adaptera (Research, ML Engine, Kaggle Master, Guardian) na Kaggle T4 GPU. 

## User Review Required
> [!IMPORTANT]
> **Promena strategije (Pivoting)**: Prethodni pokušaji treniranja sva 4 adaptera u jednom notebook-u su fejlovali nakon 110 minuta (verovatno OOM ili timeout). Prelazimo na **paralelni/izolovani pristup**: 4 odvojena notebook-a, svaki za po jendog agenta. Ovo je sigurnije, brže (svaki traje ~25 min) i lakše za debagovanje.

## Proposed Changes

### [Kaggle Notebooks]

#### [NEW] [trinity-train-research](file:///home/kizabgd/Desktop/Istrazivanje/kaggle_notebooks/trinity-train-research/trinity-train-research.ipynb)
Fokusiran isključivo na akademsko istraživanje i kardiološke formule.

#### [NEW] [trinity-train-ml-engine](file:///home/kizabgd/Desktop/Istrazivanje/kaggle_notebooks/trinity-train-ml-engine/trinity-train-ml-engine.ipynb)
Specijalizovan za feature engineering i ensemble modele.

#### [NEW] [trinity-train-kaggle-master](file:///home/kizabgd/Desktop/Istrazivanje/kaggle_notebooks/trinity-train-kaggle-master/trinity-train-kaggle-master.ipynb)
Znanje o Kaggle community-ju i anti-patternima.

#### [NEW] [trinity-train-guardian](file:///home/kizabgd/Desktop/Istrazivanje/kaggle_notebooks/trinity-train-guardian/trinity-train-guardian.ipynb)
Validacija, ProcessGuard i ustavna pravila.

---

### [Local Verification Scripts]

#### [MODIFY] [trinity_inference.py](file:///home/kizabgd/Desktop/Istrazivanje/scripts/trinity_inference.py)
Ažurirati da podržava učitavanje specifičnog adaptera po izboru, umesto da pretpostavlja da su svi u jednom folderu.

---

## Verifikacioni Plan

### Automatski testovi
- Pokretanje sva 4 notebook-a na Kaggle istovremeno.
- Provera statusa preko `kaggle kernels status`.
- Provera da li su `.safetensors` fajlovi prisutni u `/kaggle/working/` svakog kernela.

### Manuelna Verifikacija
- Korisnik preuzima 4 foldera sa adapterima.
- Pokretanje lokalne inferencije: `python scripts/trinity_inference.py --agent research`.
- Provera odgovora — da li agent prepoznaje specifične kardiološke formule (npr. Tanaka).
