# Trinity Operational Architecture Implementation Plan

This plan details the technical steps to transform the Trinity project from a mock implementation into a real, production-ready system.

## Proposed Changes

### Configuration & Core
#### [MODIFY] `trinity/config/trinity_config.yaml`
- Add settings for `AES_KEY_SOURCE` (e.g., env var).
- Add specific `reasoning_levels` mapping for the RAG phase.
- Add deployment settings: `target_p95_latency`, `reindex_threshold`.

#### [MODIFY] `trinity/main_trinity.py`
- Connect all 5 phases sequentially: Ingestion -> RAG -> AST -> Security -> Deploy.
- Phase outputs will be passed to subsequent phases instead of simple print statements.
- Add `argparse` support to allow running individual phases (e.g., `--phase 2`).

---

### Phase 1: Ingestion & Foundation
#### [MODIFY] `trinity/phases/phase1_ingestion.py`
- Implement robust parsing and validation of the `GEMINI.md` constitution.
- Add logic to verify that critical sections (e.g., Protocol definition, Rules) exist and match the expected version in `trinity_config.yaml`.
- Properly mock/handle Colab dependencies (e.g., `google.colab.userdata`) gracefully when running locally.

---

### Phase 2: Hybrid RAG
#### [MODIFY] `trinity/phases/phase2_rag.py`
- Implement a real document ingestion pipeline: Read local `.md` and `.py` files, chunk them based on `chunk_size` from config, and create embeddings (using a lightweight sentence-transformer or API if configured).
- Implement an RDB layer (SQLite) to store document metadata (source path, version, timestamp).
- Implement the Hybrid Retriever function: Queries both the vector store (0.7 weight) and RDB (0.3 weight) to match the required `score = 0.7 * vector_score + 0.3 * rdb_score` formula.
- Add `select_reasoning_level(context)` to dynamically choose Slim, Standard, Pro, or Ultra based on context length/complexity.

---

### Phase 3: SOTA AST Engine
#### [MODIFY] `trinity/phases/phase3_sota_ast.py`
- Replace hardcoded string parsing with `ast.parse` applied to actual `.py` files in the `trinity/` directory.
- Extract functions, classes, and calculate basic complexity metrics (e.g., number of branches, lines of code).
- Implement `SOTADiscoveryEngine` that manages a local JSON registry (`sota_registry.json`).
- Add `compare_run_to_sota(current_config)` to compare new metric runs against the historical bests recorded in the registry.

---

### Phase 4: Security & Logs
#### [MODIFY] `trinity/phases/secure_logger.py`
- Implement real AES-256 encryption using the `cryptography.fernet.Fernet` module. The key will be securely fetched from the `TRINITY_AES_KEY` environment variable.
- Implement robust PII scrubbing using RegEx for emails, API keys, and IP addresses, masking them appropriately (e.g., `****1234`).
- Add a `secure_log(event_type, payload, user_id=None)` function to standardize log formats.

#### [MODIFY] `trinity/phases/phase4_security.py`
- Implement `gdpr_validate(entry)` to ensure no unmasked PII exists in the log payload and verify encryption status.
- Implement `run_security_audit()` to parse the `secure_audit.log`, decrypt entries, and flag potential compliance violations.

---

### Phase 5: Deployment & Scaling
#### [MODIFY] `trinity/phases/phase5_deploy.py`
- Implement a PyTorch Distributed Data Parallel (DDP) skeleton using `torch.distributed.init_process_group`.
- Provide a `train(rank, world_size)` placeholder function demonstrating multi-GPU model wrapping.
- Implement a `@measure_latency` decorator to track the execution time of critical functions (e.g., RAG queries).
- Implement a p95 latency tracker. If latency exceeds the `target_p95_latency` from config, trigger a (mocked) `schedule_reindex()` alert via `secure_log`.

---

### Documentation
#### [MODIFY] `trinity/walkthrough.md`
- Update the walkthrough to document the new, real implementations and explain how to use the CLI and view the secure logs.

## Verification Plan

### Automated Tests
1. **Security Testing**: Send a dummy payload with mock email addresses to `secure_log` and verify the output in `secure_audit.log` is both AES-256 encrypted and successfully scrubs the PII upon decryption.
2. **AST Parsing**: Run Phase 3 on `trinity/main_trinity.py` and verify it correctly lists the internal classes and functions.
3. **GDPR Validation**: Run `run_security_audit()` and assert it correctly flags intentionally injected non-compliant plaintext logs.

### Manual Verification
1. Open the project in VS Code / Terminal.
2. Export a dummy key: `export TRINITY_AES_KEY=$(python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")`.
3. Run `python3 trinity/main_trinity.py` and observe the sequential, non-mocked execution of all phases.
4. Verify SQLite database creation for the RAG phase and `sota_registry.json` for Phase 3.
