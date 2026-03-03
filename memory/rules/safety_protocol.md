---
trigger: always_on
glob: "**/*"
description: "Global Safety Protocol to prevent corruption, security risks, and low-quality code."
priority: critical
---

# GLOBAL SAFETY PROTOCOL

## 1. Anti-Corruption (File Integrity)
> [!IMPORTANT]
> **Constraint:** You are FORBIDDEN from deleting more than 50 lines of code in a single `replace_file_content` or `multi_replace_file_content` call without explicit user confirmation.
> **Action:** If a change requires >50 lines deletion, STOP and ask: "This edit deletes X lines. Proceed? (Y/N)"

## 2. Security Guardrails
> [!CAUTION]
> **Constraint:** You are DENIED permission to automatically execute the following commands:
> - `rm` (any variation)
> - `chmod` (especially `chmod -R 777`)
> - `sudo`
> **Action:** Always propose these commands for user review. NEVER set `SafeToAutoRun: true` for them.

## 3. Senior Dev Standards (Anti-Vibe-Coding)
> [!NOTE]
> **Constraint:** All code must meet production standards.
> - **Frontend:** Must include CSS styling (no unstyled HTML).
> - **Logic:** Must include try/catch blocks and proper error handling.
> - **No Placeholders:** Do not leave `pass` or `TODO` in critical paths.

## 4. Workflow Integrity
> [!TIP]
> **Constraint:** Before starting any complex task (multi-file edits, refactoring), ensure a git repository is initialized.
> **Action:** Run `git init` if not present.
