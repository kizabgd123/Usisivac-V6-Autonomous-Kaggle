---
name: generate-unit-tests
description: Smart Test Workflow that generates, runs, and self-corrects unit tests.
---

# Skill: Smart Test Generation

- Logika: Generiše test → Pokreće test (pytest) → Ako padne, čita error log → Ispravlja kod → Ponovo pokreće (Max 3 iteracije).
- Merge: Spoji logiku testiranja sa logikom refaktorisanja.
