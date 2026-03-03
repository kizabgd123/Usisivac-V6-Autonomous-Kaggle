"""
ResearchProAI — Knowledge Ingestion Engine
===========================================
Scans directories for code, docs, and configs, then ingests them
into a ChromaDB vector store for RAG-powered analysis.

Usage:
    python src/ingest.py
    python src/ingest.py --dirs /path/to/project1 /path/to/project2
"""
import os
import sys
import glob
from typing import List, Tuple
import chromadb
from chromadb.utils import embedding_functions

# ─── Configuration ───────────────────────────────────────────────
DB_DIR = "chroma_db"
COLLECTION_NAME = "knowledge_base"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
MAX_FILE_SIZE = 500_000  # 500KB
BATCH_SIZE = 100

FILE_PATTERNS = ["**/*.py", "**/*.json", "**/*.md", "**/*.txt",
                 "**/*.csv", "**/*.yml", "**/*.yaml"]
EXCLUDE_DIRS = [".git", "node_modules", "chroma_db", "__pycache__",
                "venv", "dist", "build", ".venv", "env", ".tox"]


def load_documents(search_dirs: List[str]) -> Tuple[List[str], List[dict], List[str]]:
    """Load and chunk text files from the given directories."""
    documents, metadatas, ids = [], [], []

    print(f"🔍 Scanning directories: {search_dirs}")

    all_files = []
    for base_dir in search_dirs:
        if not os.path.exists(base_dir):
            print(f"⚠️  Directory not found, skipping: {base_dir}")
            continue
        for pattern in FILE_PATTERNS:
            found = glob.glob(os.path.join(base_dir, pattern), recursive=True)
            all_files.extend(found)

    # Filter and deduplicate
    filtered = [f for f in all_files
                if not any(ex in f for ex in EXCLUDE_DIRS) and os.path.isfile(f)]
    filtered = list(set(filtered))

    print(f"📁 Found {len(filtered)} files to process.")

    for i, file_path in enumerate(filtered):
        try:
            if os.path.getsize(file_path) > MAX_FILE_SIZE:
                continue
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
                # Use a sliding window of lines to preserve code block context
                window_size = 50
                overlap = 10
                
                for j in range(0, len(lines), window_size - overlap):
                    chunk_lines = lines[j : j + window_size]
                    if not chunk_lines:
                        break
                    chunk = "".join(chunk_lines).strip()
                    if len(chunk) > 50:
                        documents.append(chunk)
                        metadatas.append({"source": os.path.abspath(file_path), "chunk_id": f"{j//(window_size-overlap)}"})
                        ids.append(f"doc_{i}_{j}")
        except Exception as e:
            print(f"❌ Error reading {file_path}: {e}")

    return documents, metadatas, ids


def ingest_data(search_dirs: List[str] = None):
    """Main ingestion pipeline."""
    if search_dirs is None:
        search_dirs = [os.getcwd()]

    print("🚀 Starting Knowledge Ingestion...")
    client = chromadb.PersistentClient(path=DB_DIR)
    ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL)
    collection = client.get_or_create_collection(name=COLLECTION_NAME, embedding_function=ef)

    docs, metas, ids = load_documents(search_dirs)
    if not docs:
        print("⚠️  No documents found.")
        return

    print(f"➕ Ingesting {len(docs)} chunks (batch size: {BATCH_SIZE})...")
    for i in range(0, len(docs), BATCH_SIZE):
        end = min(i + BATCH_SIZE, len(docs))
        collection.upsert(documents=docs[i:end], metadatas=metas[i:end], ids=ids[i:end])
        print(f"   ✅ {end}/{len(docs)}")

    print(f"🎉 Done! Collection '{COLLECTION_NAME}' now has {collection.count()} items.")


if __name__ == "__main__":
    dirs = sys.argv[1:] if len(sys.argv) > 1 else [os.getcwd()]
    ingest_data(dirs)
