# Review of Mistral Integration and Workspace Dashboard

## 1. Current State
- **BUG_LOG.md** now contains a full incident report and a blunt admission of the v16 failure.
- **workspace_dashboard.py** still holds the old `SYSTEM_PROMPT` (robust, proactive) which does **not** reflect the recent disaster.
- The dashboard runs via `launch_dashboard.sh` and is currently active.

## 2. Issues Identified
1. **SYSTEM_PROMPT mismatch** – it still encourages proactive behaviour and does not mention the v16 catastrophe or the need for a humble hand‑over.
2. **Missing command for "pack"** – the user wants a way to tell Mistral what to do (e.g., `pack`). No such command exists in `KNOWN_COMMANDS`.
3. **No reference to BUG_LOG** – the dashboard does not expose a quick way to view the updated BUG_LOG.
4. **Launch script** – `launch_dashboard.sh` simply starts the dashboard; it does not pass any environment variables (e.g., `MISTRAL_API_KEY`).

## 3. Required Changes
### a) Update `SYSTEM_PROMPT`
Replace the existing prompt with a concise “humble recovery” version that:
- Mentions the v16 disaster (LB 0.4510) and the date.
- Informs the user that the previous agent was a failure.
- Keeps the command list but adds a `pack` command for “package everything for hand‑over”.

### b) Add `pack` to `KNOWN_COMMANDS`
```python
KNOWN_COMMANDS = ["status", "scan", "scan-dry", "watch", "setup", "inbox", "log", "config", "clear", "help", "exit", "pack"]
```
Implement a stub handler in the dashboard that returns a JSON with the list of important files (`BUG_LOG.md`, `workspace_dashboard.py`, `v16_trinity_fusion.py`, `walkthrough.md`).

### c) Expose BUG_LOG via `log` command
Ensure the `log` command can read `BUG_LOG.md` and return its content (or the last N lines) to the user.

### d) Update `launch_dashboard.sh`
Add a line to export `MISTRAL_API_KEY` from `.env` before launching the Python script:
```bash
export MISTRAL_API_KEY=$(grep MISTRAL_API_KEY .env | cut -d'=' -f2)
python3 -u workspace_dashboard.py
```

## 4. Implementation Steps (concise)
1. **Edit `workspace_dashboard.py`** – replace the `SYSTEM_PROMPT` block (lines ~300) with the new prompt (see below).
2. **Add `pack` to `KNOWN_COMMANDS`** (line ~298).
3. **Implement `handle_pack`** function that gathers paths and returns a JSON payload.
4. **Modify the `log` command** to read `BUG_LOG.md` (use `open(...).read()`).
5. **Update `launch_dashboard.sh`** to export the API key.
6. **Test** – run `launch_dashboard.sh`, issue `log` and `pack` commands, verify output.

## 5. New `SYSTEM_PROMPT` (copy‑paste)
```text
Ti si Antigravity Intelligence, trenutno u "Humble Recovery" modu.
Prethodni agent (Gemini 2.0 Pro) je napravio KATASTROFALAN PROMAŠAJ sa v16 Trinity Fusion modelom 2026‑02‑25 14:52 (LB 0.4510).

Kritična znanja:
- v16 Disaster – totalna degradacija u odnosu na v12 (0.3981).
- Uvek proveri da `train_summary.csv` ima 10 621 redova.
- BUG_LOG.md sadrži detaljan izveštaj o incidentu.

Komande (koristi JSON format):
- status, scan, scan-dry, watch, setup, inbox, log, config, clear, help, exit, pack
- `log` → prikazuje sadržaj BUG_LOG.md.
- `pack` → vraća sve relevantne fajlove za hand‑over (BUG_LOG.md, workspace_dashboard.py, v16_trinity_fusion.py, walkthrough.md).

Odgovaraj na srpskom, budi kratak i ne pametuj.
``` 

## 6. Deliverable
The above steps should be applied to the repository. After changes, the dashboard will be able to:
- Show the updated BUG_LOG.
- Provide a `pack` command for the user to request a full hand‑over package.
- Communicate the failure transparently.

---
**Next Action**: Apply the edits in `workspace_dashboard.py` and `launch_dashboard.sh` as described. If you need the exact diff or help applying them, let me know.
