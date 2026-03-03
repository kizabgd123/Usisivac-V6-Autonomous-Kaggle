---
name: code-style-guide
type: rule
scope: global
status: active
created: 2026-01-02
---

# Global Code Style Guide

## 1. Python Standards
- **Style**: Follow **PEP 8** strictly.
- **Formatter**: Use `black` or `autopep8` if available.
- **Imports**: Group imports: Standard Library > Third Party > Local Application.
- **Type Hinting**: MUST use type hints for function arguments and return values.
  ```python
  def calculate_score(leads: list[dict]) -> int:
  ```

## 2. Project Structure
- **Scripts**: Standalone scripts go in `scripts/` or root if critical (e.g., `bulk_email_sender.py`).
- **Modules**: Reusable logic goes in `src/`.
- **Tests**: All tests go in `tests/` and use `pytest`.

## 3. Error Handling & Logging
- **No Silent Failures**: Never use bare `except: pass`. Always log the error.
- **Logging**: Use the `logging` module instead of `print` for production code.
  ```python
  import logging
  logging.basicConfig(level=logging.INFO)
  logging.info("Processing started...")
  ```

## 4. Documentation
- **Docstrings**: Every function and class MUST have a docstring (Google or NumPy style).
- **README**: Every major component (directory) should have a `README.md`.

## 5. Security
- **Secrets**: NEVER hardcode API keys or passwords. Use environment variables (`os.getenv`).
- **Validation**: Always validate external inputs (CSVs, JSONs) before processing.
