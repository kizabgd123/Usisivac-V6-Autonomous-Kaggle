"""
ResearchProAI — Agent Audit Ingestion
======================================
Ingests agent work logs, guard logs, and audit reports into a
separate ChromaDB collection for forensic analysis.

Usage:
    python src/audit_ingest.py
    python src/audit_ingest.py /path/to/logs
"""
import os
import sys
import glob
import chromadb
from chromadb.utils import embedding_functions

# ─── Configuration ───────────────────────────────────────────────
DB_DIR = "chroma_db"
COLLECTION_NAME = "agent_history"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

LOG_PATTERNS = ["**/WORK_LOG.md", "**/GUARD_LOG.md", "**/*_LOG.md",
                "**/audit*.md", "**/report*.md"]


def load_audit_logs(search_dirs):
    """Load and split agent logs by markdown headers."""
    documents, metadatas, ids = [], [], []

    all_logs = []
    for base_dir in search_dirs:
        if not os.path.exists(base_dir):
            continue
        for pattern in LOG_PATTERNS:
            found = glob.glob(os.path.join(base_dir, pattern), recursive=True)
            all_logs.extend(found)

    all_logs = list(set(all_logs))
    print(f"📝 Found {len(all_logs)} log files.")

    for i, file_path in enumerate(all_logs):
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                sections = [s.strip() for s in content.split("##") if len(s.strip()) > 50]
                for j, section in enumerate(sections):
                    documents.append(section)
                    metadatas.append({
                        "source": os.path.abspath(file_path),
                        "type": "agent_report",
                        "filename": os.path.basename(file_path)
                    })
                    ids.append(f"audit_{i}_{j}")
        except Exception as e:
            print(f"❌ Error reading {file_path}: {e}")

    return documents, metadatas, ids


def ingest_audits(search_dirs=None):
    """Ingest agent logs into a dedicated collection."""
    if search_dirs is None:
        search_dirs = [os.getcwd()]

    print("🚀 Starting Agent Audit Ingestion...")
    client = chromadb.PersistentClient(path=DB_DIR)
    ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL)
    collection = client.get_or_create_collection(name=COLLECTION_NAME, embedding_function=ef)

    docs, metas, ids = load_audit_logs(search_dirs)
    if not docs:
        print("⚠️  No audit logs found.")
        return

    collection.upsert(documents=docs, metadatas=metas, ids=ids)
    print(f"✅ Audit Ingestion Complete! Collection '{COLLECTION_NAME}' has {collection.count()} items.")


if __name__ == "__main__":
    dirs = sys.argv[1:] if len(sys.argv) > 1 else [os.getcwd()]
    ingest_audits(dirs)
