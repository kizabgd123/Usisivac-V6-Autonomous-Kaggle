# Fix LLM Agent Ecosystem — Usisivač + Boardroom + JudgeGuard

Kompletna popravka svih LLM agen komponenti. Pronađeno 10+ bagova koji sprečavaju funkcionisanje celog sistema.

## Proposed Changes

---
### A. Usisivač VetoBoard Module

Kritični bagovi koji sprečavaju rad VetoBoard review modula.

#### [MODIFY] [llm_vetoboard_review.py](file:///home/kizabgd/Desktop/new-challenge/Usisivac/src/review_modules/llm_vetoboard_review.py)

**Fix 1 — `genai` import crash:** `google.generativeai` se importuje u `try/except` ali se koristi na liniji 42 i 90 bez provere. Ako paket nije instaliran ali je `vetoboard_enabled: true` → crash.
```diff
 try:
     import google.generativeai as genai
+    _GENAI_AVAILABLE = True
 except ImportError:
-    pass
+    _GENAI_AVAILABLE = False
```
Zatim proveriti `_GENAI_AVAILABLE` pre upotrebe.

**Fix 2 — Broken config import:** Linija 25-28 pokušava `from config import load_json_safe` — ali `config.py` NEMA ovu funkciju! Uvek pada u `except` i koristi prazan dict.
```diff
-try:
-    from config import load_json_safe
-    trinity_cfg = load_json_safe("../../trinity_config.json")
-except:
-    trinity_cfg = {}
+PROJECT_ROOT = Path(__file__).resolve().parents[3]
+trinity_cfg_path = PROJECT_ROOT / "trinity_config.json"
+try:
+    with open(trinity_cfg_path, 'r') as f:
+        trinity_cfg = json.load(f)
+except (FileNotFoundError, json.JSONDecodeError):
+    trinity_cfg = {}
```

**Fix 3 — Key mismatch:** `review_engine.py` šalje dict sa ključem `"path"`, ali ovaj modul traži `"file_path"`. Rezultat: `file_path = None`.
```diff
-file_path = file_analysis.get("file_path")
-content = file_analysis.get("content", "")
+file_path = file_analysis.get("path", file_analysis.get("file_path", "unknown"))
+content = file_analysis.get("content", "")
```

**Fix 4 — Content truncation:** Dodati limit od 15000 karaktera da se ne šalju ogromni fajlovi na API.

---
#### [MODIFY] [review.py](file:///home/kizabgd/Desktop/new-challenge/Usisivac/src/review.py)

**Fix 5 — Default categories:** `vetoboard` je uključen po defaultu → svaki review poziva Gemini API. Treba biti opt-in.
```diff
-"--categories", default="security,performance,quality,vetoboard"
+"--categories", default="security,performance,quality"
```

---
### B. JudgeGuard

#### [MODIFY] [judge_guard.py](file:///home/kizabgd/Desktop/new-challenge/judge_guard.py)

**Fix 6 — Absolute path:** `Usisivac/src/review.py` je relativna putanja. Koristiti `os.path.dirname(__file__)` za baznu putanju.
```diff
+SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
 veto_check = subprocess.run(
-    ["python", "Usisivac/src/review.py", ".", "--categories", "vetoboard", "--output-format", "json"],
+    [sys.executable, os.path.join(SCRIPT_DIR, "Usisivac/src/review.py"),
+     SCRIPT_DIR, "--categories", "vetoboard", "--output-format", "json"],
     capture_output=True, text=True
 )
```

**Fix 7 — JSON parsing:** Umesto krhkog string matching-a na stdout, parsirati JSON output.
```diff
-if "Total Issues Found: 0" not in veto_check.stdout and "VETO TRIGGERED" in veto_check.stdout:
+try:
+    veto_data = json.loads(veto_check.stdout)
+    veto_issues = sum(len(r.get("issues", [])) for r in veto_data.get("results", []))
+    has_veto = any("VETO" in str(issue) for r in veto_data.get("results", []) for issue in r.get("issues", []))
+except (json.JSONDecodeError, TypeError):
+    has_veto = "VETO TRIGGERED" in veto_check.stdout  # fallback
+if has_veto:
```

---
### C. Boardroom Advisor

#### [MODIFY] [boardroom_advisor.py](file:///home/kizabgd/Desktop/new-challenge/boardroom_advisor.py)

**Fix 8 — Wrong config key:** Koristi `vetoboard_enabled` umesto sopstvenog ključa.
```diff
-if not llm_config.get("vetoboard_enabled", False):
+if not llm_config.get("boardroom_enabled", False):
```

---
### D. Configuration

#### [MODIFY] [trinity_config.json](file:///home/kizabgd/Desktop/new-challenge/trinity_config.json)

**Fix 9 — Missing boardroom key:**
```diff
 "llm_agents": {
     "vetoboard_enabled": true,
-    "model": "gemini-2.5-flash"
+    "boardroom_enabled": true,
+    "model": "gemini-2.5-flash"
 }
```

---
---
### E. Usisivač RAG Optimization

Pronađeno je da RAG sistem ne vadi dovoljno specifične informacije za s6e3 takmičenje iako su notebook-ovi prisutni.

#### [MODIFY] [generate_report.py](file:///home/kizabgd/Desktop/new-challenge/Usisivac/src/generate_report.py)

**Fix 10 — Increase Retrieval Depth:** Povećati `n_results` sa 5 na 15 kako bi LLM imao širi kontekst iz različitih notebook-ova.
**Fix 11 — Prompt Engineering:** Poboljšati sistemski prompt da LLM aktivno traži s6e3 specifične labele u dostavljenom kontekstu.

## Verification Plan (Updated)

### Automated Tests
...
6. **RAG Integration Test**: Pokrenuti pretragu za "s6e3 totalcharges engineering" i potvrditi da Gemini vidi specifične transformacije iz `ps-s6e3-xgb-lgm-lr-with-100-oofs-0-91665.txt`.
