# LLM Agentic Legal Information Retrieval - Grandmaster Plan

## Goal
Retrieve the right Swiss legal sources (mostly German) for English legal questions. Optimize citation-level Macro F1 on a hidden test set in an offline Kaggle environment. 

## Strategy Overview: The Hybrid Agentic Pipeline
Drawing from elite strategies in previous competitions (Target Feature Extraction in Melting Point, XGBoost meta-learners in House Prices, DART ensembles in Heart Disease, and offline fallbacks in Deep Past), the ultimate strategy for this IR task is a **4-Phase Hybrid Pipeline**:

### Phase 1: Query Expansion & Translation (The "Agentic" Part)
- English queries and German corpus pose a lexical gap for sparse retrieval (BM25).
- **Action**: Use a lightweight LLM (e.g., `Qwen2.5-1.5B` or `Gemma-2B`) to rewrite the English query into a detailed German legal query (Query Translation) AND generate a hypothetical Swiss legal answer (HyDE: Hypothetical Document Embeddings).

### Phase 2: Multi-Vector Hybrid Retrieval
- **Sparse**: BM25 configured for the German language, applied to the translated query and corpus.
- **Dense**: `BAAI/bge-m3` (State-of-the-Art Multi-Lingual Embeddings). It natively maps English queries to German documents.
- **Fusion**: Reciprocal Rank Fusion (RRF) combines BM25 ranks and BGE-M3 ranks to recall the top 100 candidate citations.

### Phase 3: Heavyweight Cross-Encoder Reranking
- Pass the (Query, Candidate Document) pairs through a highly accurate Cross-Encoder to compute exact relevance scores.
- **Model**: `BAAI/bge-reranker-v2-m3` or a fine-tuned `XLM-RoBERTa`. This bridges the final semantic gap and provides highly calibrated logits.

### Phase 4: XGBoost / CatBoost F1 Optimizer (The "Grandmaster Meta-Learner")
- Pure similarity scores don't directly optimize F1 (where false positives penalize precision).
- **Action**: Extract features for each candidate (Dense Score, Sparse Rank, Cross-Encoder Score, Document Length, Query Length) and train an **XGBoost Classifier using DART** to predict if a citation is a Gold Citation (1 or 0).
- Dynamically select the optimal probability cutoff that maximizes Macro F1 on our validation set.

## Task Checklist
- [x] Implement robust `Config` structure for offline datasets and API usage.
- [x] Create Corpus Indexing script (BM25 + FAISS Dense, handling 2.4GB considerations).
- [x] Implement HyDE and Query Translation logic using lightweight LLMs.
- [x] Implement RRF (Reciprocal Rank Fusion) for phase 2 hybrid retrieval.
- [x] Add BGE-M3 Cross-Encoder Reranking loop.
- [x] Extract Meta-Features and train the XGBoost F1 Threshold model.
- [/] Submit notebook to Kaggle and verify Offline execution.
