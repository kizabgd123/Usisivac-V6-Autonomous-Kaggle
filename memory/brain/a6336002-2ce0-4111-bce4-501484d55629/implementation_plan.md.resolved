# Populate Project Skills from External Infrastructure

The goal is to populate the current workspace (`/home/kizabgd/Desktop/kaggle-arena/`) with the suite of 20 skills identified in the global `.gemini` infrastructure and project-specific work logs. This will align the current project with the **Trinity Protocol v4.0** and the **Master Orchestration Protocol**.

## Proposed Changes

### [Core Structure]

#### [NEW] [.agent/](file:///home/kizabgd/Desktop/kaggle-arena/.agent/)
- Initialize the `.agent/` directory with `skills/` and `workflows/` subdirectories.

### [Skill Migration]

#### [NEW] [.agent/skills/](file:///home/kizabgd/Desktop/kaggle-arena/.agent/skills/)
I will populate the following skills by transforming source files from `.gemini/antigravity/` and scratch project locations:

1. **extract_emails**: Migrate from `prikupljanje_informacija`.
2. **web-scraper**: Migrate from global `.gemini` skills directory.
3. **agent-discipline-protocol**: Migrate from global `.gemini` skills directory.
4. **agent-forensics-and-hardening**: Migrate from `Istrazivanje` system skills.
5. **mentorstvo/analysis**: Migrate from `Istrazivanje` system skills.
6. **generate-unit-tests**: Migrate from global `.gemini` skills directory.
7. **code-style-guide**: Migrate from global `.gemini` skills directory.

> [!NOTE]
> For skills listed in `SKILL_MANIFEST.json` that lack an obvious `skill.md` source, I will attempt to "harvest" them from the mentioned script paths (e.g., `generate_backups.py`, `build_squad.py`) if they exist in the referenced project directories.

## Verification Plan

### Automated Tests
- No automated tests are applicable for document population, but I will verify file existence and structure using `ls -R`.
- I will run `python3 judge_guard.py "Identity Verification"` if available to check protocol compliance.

### Manual Verification
- The user can verify that the `.agent/skills/` directory is populated and that `SKILL.md` files are properly formatted with high-quality descriptions.
