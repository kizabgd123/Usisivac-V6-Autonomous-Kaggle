"""
Code Review Pattern Ingestor
============================
Specialized ingestion script for code review patterns, security best practices,
and performance optimization rules.
"""
import os
import chromadb
from chromadb.utils import embedding_functions

# ─── Configuration ───────────────────────────────────────────────
DB_DIR = "chroma_db"
COLLECTION_NAME = "code_review_patterns"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

REVIEW_PATTERNS = [
    {
        "id": "sec_001",
        "title": "SQL Injection Prevention",
        "content": "Always use parameterized queries or ORM methods instead of string concatenation for SQL queries. Avoid direct use of execute() with f-strings or % formatting.",
        "category": "security",
        "severity": "high"
    },
    {
        "id": "sec_002",
        "title": "XSS Prevention",
        "content": "Sanitize all user input before rendering in HTML. Use templates that auto-escape or explicit sanitization libraries. Avoid innerHTML with untrusted data.",
        "category": "security",
        "severity": "high"
    },
    {
        "id": "perf_001",
        "title": "N+1 Query Optimization",
        "content": "Batch database queries instead of executing one query per item in a loop. Use 'select_related' or 'prefetch_related' in ORMs.",
        "category": "performance",
        "severity": "medium"
    },
    {
        "id": "qual_001",
        "title": "Error Handling Patterns",
        "content": "Avoid bare 'except:' clauses. Always catch specific exceptions and log them or handle them gracefully.",
        "category": "quality",
        "severity": "medium"
    }
]

def ingest_review_patterns():
    print("🚀 Ingesting Code Review Patterns...")
    client = chromadb.PersistentClient(path=DB_DIR)
    ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL)
    collection = client.get_or_create_collection(name=COLLECTION_NAME, embedding_function=ef)

    documents = [p["content"] for p in REVIEW_PATTERNS]
    metadatas = [{"title": p["title"], "category": p["category"], "severity": p["severity"]} for p in REVIEW_PATTERNS]
    ids = [p["id"] for p in REVIEW_PATTERNS]

    collection.upsert(documents=documents, metadatas=metadatas, ids=ids)
    print(f"🎉 Ingested {len(ids)} patterns into '{COLLECTION_NAME}'.")

if __name__ == "__main__":
    ingest_review_patterns()
