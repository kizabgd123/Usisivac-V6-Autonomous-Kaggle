# Mistral VetoBoard (Guardian) Integration

Povezivanje Mistral API-ja sa `GEMINI.md` pravilima u cilju stvaranja zaštitnog mehanizma ("VetoBoard") koji kontroliše i savetuje agente.

## 1. Analiza pristupa: HuggingFace Fine-Tuning vs. LLM Prompt Engineering

> [!TIP]
> **Preporuka:** Nema potrebe za kompleksnim i skupim fine-tuningom na HuggingFace-u da bi model naučio pravila. `GEMINI.md` Ustav je prilično kratak (~300 linija) i može se vrlo efikasno preneti Mistral modelu kroz **System Prompt** (Context Window) pri svakom API pozivu.

Ovo je **mnogo bolje** iz tri razloga:
1. Nula dolara troška (Mistral Small Free API je više nego dovoljan za prosleđivanje celog teksta Ustava).
2. Nema potrebe za održavanjem eksternih HuggingFace repozitorijuma; kada god se `GEMINI.md` promeni, Mistral to automatski pročita uživo.
3. Potpuna kontrola nad `max_tokens` (limit) u samoj skripti, čime se štiti besplatni API limit.

---

## 2. Predložene Arhitektonske Promene

### 1. `scripts/mistral_guardian.py`
Novi Python skript koji predstavlja "mozak" VetoBoard-a.
- Učitava vaš `MISTRAL_API_KEY` iz `.env` fajla.
- Učitava kompletan sadržaj `GEMINI.md` kao ustav/zakon.
- Šalje Mistral API-ju zahtev u kom ga instrukcijama primorava da bude strog "Guardian" sudija.
- **Bezbednosni limit:** Output će biti fiksiran na maksimalno `150 tokena` (par rečenica). Nema halucinacija, model će odgovarati veoma kratko u formatu `[PASS] / [VETO]` uz jednu rečenicu objašnjenja.

### 2. `Makefile` Integracija
Dodavanje meta komande u `Makefile`:
```makefile
mistral:
	@python3 scripts/mistral_guardian.py "$(query)"
```
Ovo omogućava agentu (ili Vama) da vrlo brzo pita model za savet iz celog workspace-a, npr: `make mistral query="Pokušavam da obrišem sve CSV fajlove da smanjim prostor, da li je to okej?"`

### 3. Workflow fajl: `.agents/workflows/mistral_trigger.md`
Zvanična registracija `!Mistral` ili `/Mistral` komande.
Ovaj fajl je "skill" koji daje eksplicitnu instrukciju Agentu (meni, koji izvršavam radnje). Kada ukucate `!Mistral`, ja **moram** da prekinem ono što radim, uzmem vaš tekst i prosledim ga fajlu `mistral_guardian.py`. Zatim, na osnovu onoga što je Mistral vratio (njegovog sudskog mišljenja o ustavu `GEMINI.md`), ja biram da li nastavljam rad ili odustajem.

---

## 3. Način upotrebe

Kada završimo implementaciju, komunikacija će izgledati ovako:

**Vi:** `!Mistral da li smem da spojim ova 3 modela iako imaju veliku korelaciju?`

**Agent (Ja):** *[Preuzimam upit i proleđujem ga Mistralu ispod haube preko API-ja]*

**Mistral (Sudija):**
`[VETO]: Ovo je direktno kršenje Pravila 10 iz GEMINI.md. Ako modeli imaju veliku korelaciju, njihovo spajanje u ansambl samo pojačava postojeće greške i šum (Overfitting). Predložite ortogonalniji model.`

**Agent (Ja):** `Mistral nam je izdao VETO. Ne mogu da izvršim spajanje. Pokušaću da pronađem nezavisniji model.`
