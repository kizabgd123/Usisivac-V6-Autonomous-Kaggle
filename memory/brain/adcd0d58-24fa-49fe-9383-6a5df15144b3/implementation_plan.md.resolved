# 🏗️ Implementation Plan: Bidding Resurrection (Quad-Core)

Recover from the v16 regression by establishing a robust agentic infrastructure and a verified forensic analysis.

## Proposed Changes

### ⚖️ Core 4: The Law (Orchestration)
#### [NEW] .agent/ (directory)
Instantiate the project-level orchestration structure:
- `.agent/rules/`
- `.agent/workflows/`
- `.agent/skills/`

#### [NEW] WORK_LOG.md
Continuous activity tracking following the `MASTER_ORCHESTRATION.md` template.

---

### 🧠 Core 1: The Brain (Agentic Dashboard)
#### [MODIFY] [workspace_dashboard.py](file:///home/kizabgd/Desktop/Istrazivanje/workspace_dashboard.py)
Transform into **Dashboard 3.0 (Agentic Mode)**:
- **Tool Definition:** JSON schema for `bash`, `read_file`, `write_file`, `list_dir`.
- **Tool Loop:** Middleware to detect Mistral tool calls, ask for confirmation, execute, and return results to the AI.

---

### 🛡️ Core 3: The Shield (Integrity)
#### [NEW] [judge_guard.py](file:///home/kizabgd/Desktop/Istrazivanje/construction_bidding/judge_guard.py)
Project-local instantiation of the Shield.
- Pre-action checks for dataset row counts (10,621).
- Veto logic for regression signatures.

---

---

### 🔑 Core 5: API Infrastructure (Rotating Keys)
#### [MODIFY] .env
Add four new Gemini API keys provided by the user: `GEMINI_KEY_1`, `GEMINI_KEY_2`, `GEMINI_KEY_3`, `GEMINI_KEY_4`.

#### [MODIFY] [ORCHESTRATION_RULES.json](file:///home/kizabgd/Desktop/Istrazivanje/.agent/rules/ORCHESTRATION_RULES.json)
- Update `model` to `gemini-2.0-flash`.
- Ensure `rotation_strategy` is set to `round_robin`.

#### [MODIFY] [gemini_client.py](file:///home/kizabgd/Desktop/Istrazivanje/src/antigravity_core/gemini_client.py)
- Refactor `GeminiClient` to load all `GEMINI_KEY_*` variables from `.env`.
- Implement `get_next_key()` logic based on a shared counter.
- Hardcode or configure `genai` to use `gemini-2.0-flash`.
- Improve error handling to rotate keys immediately on `429` (Quota Exceeded).

---

## Verification Plan

### Automated Tests
- `pytest tests/test_dashboard_tools.py` — Verify tool-loop parsing and safety.
- `python3 construction_bidding/judge_guard.py --status` — Verify Shield status.

### Manual Verification
- Test `chat` mode in dashboard by asking "Šta piše u BUG_LOG.md — pročitaj fajl direktno".
- Verify that Mistral can now "see" file contents via tools.
