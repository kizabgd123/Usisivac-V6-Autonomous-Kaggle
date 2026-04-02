# 🚢 Usisivac V6: Autonomous Multi-Agent Intelligence Protocol

## 🏛️ Arhitektura Sistema
Usisivac V6 nije statična skripta, već **živi ekosistem autonomnih agenata** koji sarađuju putem centralnog orkestratora. Sistem je dizajniran da pretvori sirovo istraživanje (RAG) u funkcionalan, produkcioni kod bez ljudske intervencije.

### 🤖 Agent Pool
1.  **🔎 ResearchAgent**: Pretražuje ChromaDB bazu znanja (kernels, documentation, solutions) i kreira strukturirane izveštaje o najboljim praksama.
2.  **🛡️ CriticAgent**: Identifikuje "zamke" (anti-patterns) i zablude koje mogu degradirati score. Služi kao korektivni faktor za istraživanje.
3.  **🤖 CoderAgent (V6)**: Srce sistema. Uzima izveštaje od Research i Critic agenata i **samostalno piše Python kod** (`generated_features.py`) koristeći LLM (Gemini/Mistral).
4.  **🧹 CleanerAgent**: Automatski čisti podatke (outliers, imputation, naming) koristeći robustne statističke metode.
5.  **⚙️ FeatureAgent (V6)**: Dinamički učitava kod koji je `CoderAgent` napisao i izvršava ga nad podacima.

## 🔑 Key Rotation & Resiliency
Sistem implementira **automatsku rotaciju API ključeva** kako bi se izbegao Rate Limit (429):
- Rotira kroz 5 različitih Gemini ključeva.
- Automatski prelazi na **Mistral (Pixtral-Large)** kao finalni fallback ako svi Gemini ključevi dostignu kvotu.

## 🏆 Golden Recipe (S6E3 Breakthrough)
Za Telco Churn challange, Usisivač je samostalno identifikovao i implementirao:
- **Original Data Target Lookups**: Mapiranje verovatnoća churn-a iz istorijskih IBM podataka na sintetički set.
- **Frequency Encoding**: Identifikacija retkih kategorija kao signala.
- **Financial Ratios**: Odstupanje realnih troškova od teoretskih.
- **Rank Blending**: Obavezna stabilizacija pri spajanju različitih modela.

---
*Protokol odobren od strane Grandmaster-a.*
