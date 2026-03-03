# Goal Description
Integrate Large Language Models (LLMs) into the Trinity Protocol to act as a strategic advisor ("Boardroom") and a strict code auditor ("Usisivač/LLM VetoBoard"). The goal is to automate the analysis of tabular machine learning iterations and rigorously enforce the rules defined in `GEMINI.md`.

## Proposed Changes

---
### The Boardroom (Strategic Advisor Agent)
A new script that collects current project telemetry (OOF scores, correlation matrices, `trinity_config.json`) and asks the Gemini API for the next best tactical move in the competition.

#### [NEW] `boardroom_advisor.py`
- Gathers data from:
  - `final_score.txt` / output of recent runs
  - `GUARD_ALERT.json` (if any alerts were triggered)
  - `trinity_config.json`
- Formats this data into a comprehensive prompt.
- Calls the Gemini API (`google.generativeai`).
- Outputs the strategic advice to `BOARDROOM_STRATEGY.md` and prints it to the console.

---
### Usisivač (LLM VetoBoard / Auditor)
Enhance the existing `Usisivac` and `judge_guard.py` systems to perform LLM-powered code review before submission or training.

#### [NEW] `Usisivac/src/review_modules/llm_vetoboard_review.py`
- A new review module for the existing `Usisivac` system.
- Reads the Python script to be reviewed.
- Checks it against rules from `GEMINI.md` (e.g., "Anti-Regression Manifesto", checks for data leakage).
- If the LLM returns "VETO", the module fails the review.

#### [MODIFY] `Usisivac/src/review.py`
- Register `llm_vetoboard_review.py` as an available, opt-in category (e.g., `--categories quality,security,vetoboard`).

#### [MODIFY] `judge_guard.py`
- Add an 8th Gate: **LLM Veto Gate**.
- Before passing the CSV as safe, trigger a quick LLM sanity check (or invoke the `Usisivac` review script programmatically) if a new script was modified.

---
### Configuration Updates
#### [MODIFY] `trinity_config.json`
- Add a new block `"llm_agents": { "vetoboard_enabled": true, "model": "gemini-2.5-flash" }` to control the integration parameters without hardcoding them.

## Verification Plan

### Automated Tests
- Run `python Usisivac/src/review.py /path/to/test_script.py --categories vetoboard` on an intentionally bad script (e.g., one with data leakage) to verify the VETO is triggered.
- Run `python boardroom_advisor.py` to ensure it successfully generates `BOARDROOM_STRATEGY.md` with relevant Kaggle advice.
- Run `python judge_guard.py` on a dummy submission to ensure the new gates do not break existing functionality.

### Manual Verification
- Review the generated `BOARDROOM_STRATEGY.md` to ensure the advice is strategically sound for a Tabular ML competition.
