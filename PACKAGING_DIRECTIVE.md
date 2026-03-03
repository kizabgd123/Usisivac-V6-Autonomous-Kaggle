# 📡 Directive for Agent IDE: GitHub Deployment

**Status**: RESEARCH & CRITIC phases complete. PROTOTYPE V6 SUCCESSFUL.
**Goal**: Package Usisivac V6 for GitHub.

### 📋 Steps to Execute:
1.  **Repository Setup**:
    - Folder: `usisivac_work_pack/`
    - Initialise Git: `git init`
    - Create `.gitignore`:
      ```
      .env
      data/*.csv
      chroma_db/
      __pycache__/
      *.zip
      ```
2.  **Verification**:
    - Ensure `Usisivac/src/generate_report.py` has the key rotation logic (from V6).
    - Ensure `Usisivac/src/orchestrator.py` references `CoderAgentV6`.
3.  **Commit**:
    - Message: "feat: Usisivac V6 Autonomous Multi-Agent Intelligence System"
4.  **Final Push**:
    - Target: GitHub (as directed by user).

---
*End of Directive.*
