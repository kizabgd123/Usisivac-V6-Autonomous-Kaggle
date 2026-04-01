import os
import subprocess
import sys
import chromadb
from chromadb.utils import embedding_functions
from Usisivac_2.src.ingest import load_documents
from dotenv import load_dotenv

load_dotenv()

# ─── Configuration ───────────────────────────────────────────────
EXTERNAL_SOURCES_DIR = "memory/external_sources"
DB_DIR = "chroma_db"
COLLECTION_NAME = "knowledge_base"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
BATCH_SIZE = 100

REPOSITORIES = {
    "OpenHands": "https://github.com/All-Hands-AI/OpenHands",
    "aider": "https://github.com/Aider-AI/aider",
    "Cline": "https://github.com/cline/cline",
    "judge-guard-core": "https://github.com/kizabgd123/judge-guard-core",
    "Usisivac": "https://github.com/kizabgd123/Usisivac",
    "bolt.new": "https://github.com/stackblitz/bolt.new"
}

def run_command(command, cwd=None):
    """Utility to run shell commands."""
    try:
        subprocess.check_call(command, shell=True, cwd=cwd)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running command '{command}': {e}")
        return False

def inhale_github():
    """Clones/Updates and ingests the target repositories."""
    os.makedirs(EXTERNAL_SOURCES_DIR, exist_ok=True)
    
    print("🚢 USISIVAC GitHub Inhaler: Starting extraction mission...")
    print("-" * 50)

    # 1. Clone or Update Repos
    for name, url in REPOSITORIES.items():
        repo_path = os.path.join(EXTERNAL_SOURCES_DIR, name)
        if os.path.exists(repo_path):
            print(f"🔄 Updating {name}...")
            run_command("git pull", cwd=repo_path)
        else:
            print(f"📥 Cloning {name}...")
            run_command(f"git clone {url} {name}", cwd=EXTERNAL_SOURCES_DIR)

    # 2. Ingest into ChromaDB
    print("\n🚀 Starting Knowledge Ingestion for External Sources...")
    client = chromadb.PersistentClient(path=DB_DIR)
    ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL)
    collection = client.get_or_create_collection(name=COLLECTION_NAME, embedding_function=ef)

    # We only ingest the external sources here
    search_dirs = [os.path.join(EXTERNAL_SOURCES_DIR, name) for name in REPOSITORIES.keys()]
    
    docs, metas, ids = load_documents(search_dirs)
    
    if not docs:
        print("⚠️ No new documents found to inhale.")
        return

    print(f"➕ Ingesting {len(docs)} chunks from external sources...")
    for i in range(0, len(docs), BATCH_SIZE):
        end = min(i + BATCH_SIZE, len(docs))
        # Add 'type: external_source' to metadata
        batch_metas = metas[i:end]
        for meta in batch_metas:
            meta['type'] = 'external_source'
            
        collection.upsert(documents=docs[i:end], metadatas=batch_metas, ids=ids[i:end])
        if end % 500 == 0:
            print(f"   ✅ {end}/{len(docs)}")

    print(f"🎉 Inhalation Complete! Collection now has {collection.count()} items.")

if __name__ == "__main__":
    inhale_github()
