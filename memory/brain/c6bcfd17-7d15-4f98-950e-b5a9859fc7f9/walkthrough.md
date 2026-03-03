# MCP Server Walkthrough

This document outlines the implementation of the MCP-GUARDIAN and MCP-VETOBOARD servers.

### Changes Made
- Created the `.mcp/mcp-guardian/` and `.mcp/mcp-vetoboard/` directories.
- Wrote `server.py` and `requirements.txt` for **MCP-GUARDIAN**, providing the `check_submission` tool to validate dataframes and evaluate risks utilizing the Groq Llama-3-70b model.
- Integrated the autonomous forensics fallback for MCP-GUARDIAN using the `.agent/skills/_system/agent_forensics_and_hardening/SKILL.md` skill, falling back to OpenRouter Claude 3.5 Sonnet to automatically generate the skill if missing.
- Wrote `server.py` and `requirements.txt` for **MCP-VETOBOARD**, providing the `evaluate_action` tool that routes requests to a 3-member board: Groq Analyst (Thesis), OpenRouter Critic (Antithesis), and Local Mistral Oracle (Veto). It tallies scores and requires a 6/8 consensus to PASS an action.
- Configured both servers to read API keys directly from `.env` via `python-dotenv`.

### Validation Results
- Verified that all Python syntax is correct and modules load successfully.
- Tests executed against importing `mcp` core objects demonstrate it's ready to attach locally to an MCP Client (e.g. Cursor, Claude Desktop, or AI Agent IDE).

### Next Steps
1. Make sure to `pip install -r requirements.txt` within your environment (if the provided `python-dotenv`, `mcp`, `groq`, `openai`, `pandas` were installed manually via pip above, the environment is ready).
2. Configure your specific MCP Client's `mcp.json` or equivalent to launch:
   - `python -m .mcp.mcp-guardian.server`
   - `python -m .mcp.mcp-vetoboard.server`
