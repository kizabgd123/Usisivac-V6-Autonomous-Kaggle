# MCP-GUARDIAN & MCP-VETOBOARD (v5.1) Implementation Tasks

- [x] Create `.mcp` directory structure
- [x] Implement MCP-GUARDIAN
  - [x] Initialize Python MCP server project in `.mcp/mcp-guardian/`
  - [x] Integrate `judge_guard.py` logic (7-Gate check)
  - [x] Define `check_submission` tool
  - [x] Implement Groq (Llama-3-70b) routing for Risk Gate / 7-Gate validation
  - [x] Integrate Forensics skill auto-invocation on failure (and OpenRouter fallback for new skills)
  - [x] Configure `mcp-config-state` to read keys from `.env`
- [x] Implement MCP-VETOBOARD
  - [x] Initialize Python MCP server project in `.mcp/mcp-vetoboard/`
  - [x] Define `evaluate_action` tool
  - [x] Implement Hybrid LLM Consensus (Groq Analyst, OpenRouter Critic, Local Mistral Oracle)
  - [x] Implement 6/8 consensus logic according to ORCHESTRATION_RULES
  - [x] Configure `mcp-config-state` to read keys from `.env`
- [x] Test and Validate
  - [x] Verify MCP-GUARDIAN starts and responds to `check_submission`
  - [x] Verify MCP-VETOBOARD starts and responds to `evaluate_action`
