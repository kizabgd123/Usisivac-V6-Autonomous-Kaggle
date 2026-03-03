# Walkthrough: Fixing Legacy Trinity Tests

## Problem Statement
The user requested a fix for `pytest` tests failing in the legacy Trinity ecosystem. The core failures were:
1. `tests/test_discovery.py` failing due to parameter extraction missing nested and simple variables from code parsing.
2. `tests/test_memory.py` failing due to missing `StrategicQueryEngine` configuration causing a crash in semantic search logic.

## Steps Taken & Changes Made

### 1. Fixed AST Parsing in `IntelligenceParser`
- **File modified:** `scripts/intelligence_parser.py`
- Added the `analyze_patterns()` method to safely search the AST for Binary Operations (multiplication/division) to capture feature engineering interaction logic.
- Added `extract_parameters_from_content()` method using AST validation and Python's `ast.Assign` and `ast.Call` nodes to parse assignments (`learning_rate = 0.01`) and kwargs (`n_estimators=1000`).
- Updated `_extract_logic()` to fallback to these two AST parsing methods if the newly implemented `SOTADiscoveryEngine` failed or missed simplistic standard variable assignments.

### 2. Fixed DB & Search Attributes in `StrategicQueryEngine`
- **File modified:** `scripts/strategic_query_engine.py` 
- Resolved the `AttributeError: 'StrategicQueryEngine' object has no attribute 'config'` by initializing `self.config = {}` in `__init__()`.
- Fixed the `search_code()` formatting logic, which initialized variables but failed to actually structure and return the `formatted` dictionary payload. Restructured to properly extract `documents`, `distances`, and `metadatas` from FAISS/Chroma search results based on Hybrid weights.
- Verified that `model_lineage` table creation was actually already present in `scripts/trinity_kb.py:120`, avoiding duplicate query injections.

## Verification
Executed Pytest locally across the suite:
```bash
pytest tests/test_discovery.py tests/test_memory.py
```
**Results:** `6 passed, 2 warnings in 20.04s`

## Database Schema Status
The quad-core RDB memory currently manages the following valid structure in `trinity_kb.db`:
- `strategies`
- `parameters`
- `board_audits`
- `model_lineage` (Verified existence on line 120 of `trinity_kb.py`)
- `kb` (Legacy fallback table)

## Key Takeaways
We successfully adhered to the `GEMINI.md` standard by reinforcing static AST analysis without relying on potentially brittle runtime imports. The query engine is now robust enough to handle mocked/empty configurations during automated CI/CD testing while maintaining the 70/30 Hybrid Vector weight formula.
