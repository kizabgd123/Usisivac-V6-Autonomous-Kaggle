# Task: End-to-End LLM Integration (Boardroom & Usisivač)

- [x] Investigate existing `Usisivac` scripts and `judge_guard.py`
- [x] Implement/Update `Usisivac` (Code Review Agent)
  - [x] Add LLM integration to analyze python code against `GEMINI.md` rules
  - [x] Integrate into `review.py` or pre-commit hooks
- [x] Implement `Boardroom` (Strategic Agent)
  - [x] Create script to read experiment results, OOF scores, and alerts
  - [x] Add LLM integration to output dynamic `task.md` or next-step advice
- [x] Update `trinity_config.json` with LLM API config or toggle
- [x] End-to-End Test of both agents
