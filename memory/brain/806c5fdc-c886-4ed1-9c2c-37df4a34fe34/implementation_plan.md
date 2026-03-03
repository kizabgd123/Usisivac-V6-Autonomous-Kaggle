# Kaggle Legal Information Retrieval - Grandmaster Implementation Plan

## Goal
To build a highly robust, offline-capable pipeline that processes English legal questions and retrieves the most relevant Swiss German laws from the provided corpus, maximizing Macro F1 via an intelligent cutoff threshold mechanism.

## Proposed Changes

### 1. Data Processing and Indexing Pipeline
- Parse `laws_de.csv` and the massive `court_considerations.csv`.
- Create a script `run_indexing.py` (or extend the existing one) to build:
  - **BM25 Index** (using `rank_bm25` with German snowball stemmer).
  - **Dense FAISS Index** using `BAAI/bge-m3` or `intfloat/multilingual-e5-base`. We must split large documents into chunks and map chunks back to their respective citations.

### 2. Query Translation & Expansion (HyDE) Component 
- Create `query_processor.py`.
- Incorporate a lightweight causal LLM (e.g., `Gemma-2B-IT` or `Qwen2.5-1.5B-Instruct`).
- **Function**: `translate_and_expand_query(english_query) -> german_query, hypothetical_document`
- This bridges the language gap allowing BM25 to perform significantly better.

### 3. Hybrid Retrieval & RRF Fusion Component
- Create `hybrid_retriever.py`.
- **Function**: `retrieve_candidates(query)`
  - Run `BM25` on `german_query`.
  - Run `Dense Search` on the original `english_query` and the `hypothetical_document` using `bge-m3`.
  - Combine the top `k=100` results using Reciprocal Rank Fusion (RRF): `score = 1 / (60 + rank_bm25) + 1 / (60 + rank_dense)`.

### 4. Cross-Encoder Reranking
- Add `cross_encoder_reranker.py`.
- Load `BAAI/bge-reranker-v2-m3` (multilingual).
- Rerank the top 100 RRF candidates based on exact sequence similarity.

### 5. F1 Threshold Optimizer (XGBoost/CatBoost)
- Pure ranks do not directly translate to F1 (which penalizes providing 10 citations if only 1 is correct).
- Create `train_f1_threshold.py`.
- **Features to Extract**: RRF Score, Cross-Encoder Logit, Dense Similarity, Sparse Score, Query Length, Document Length.
- **Target**: `Is_Gold_Citation` (Binary).
- Train an `XGBoost (DART)` classifier on the local `train.csv` and validate on `val.csv`. Find the optimal probability threshold `p_cut` that maximizes Macro F1.

### 6. Main Kaggle Submission Script
- Combine components into a single `Submission.py` script.
- Ensure all models are loaded from `/kaggle/input/...` (offline compliance).
- Format the output into `submission.csv` correctly.

## Verification Plan

### Automated Tests
- Run the full pipeline on `val.csv` locally.
- Validate F1 scores are calculated correctly and show improvements over the base `sample_submission.csv` or standard BM25 retrieval.

### Manual Verification
- Review Kaggle offline limits (Memory / Disk constraints).
- Create the dataset bundle and test a `kaggle kernels push`.
