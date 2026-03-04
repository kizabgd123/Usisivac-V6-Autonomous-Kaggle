import os
import sys
import chromadb
from chromadb.utils import embedding_functions
from Usisivac.src.skill_registry import SkillRegistry
from dotenv import load_dotenv

load_dotenv()

# Configuration
DB_DIR = "chroma_db"
COLLECTION_NAME = "knowledge_base"  # Shared with main RAG but tagged
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

def ingest_skills():
    print("🚀 Ingesting Skills into ChromaDB...")
    
    # 1. Initialize Registry & DB
    registry = SkillRegistry(skills_path="memory/skills")
    skills = registry.refresh()
    
    if not skills:
        print("⚠️ No skills found in memory/skills.")
        return

    client = chromadb.PersistentClient(path=DB_DIR)
    ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL)
    collection = client.get_or_create_collection(name=COLLECTION_NAME, embedding_function=ef)

    # 2. Prepare Data
    documents = []
    metadatas = []
    ids = []

    for name, meta in skills.items():
        # Concatenate name, description, and full content for deep search
        try:
            with open(meta['abs_path'], 'r', encoding='utf-8') as f:
                content = f.read()
            
            doc_text = f"SKILL NAME: {name}\nDESCRIPTION: {meta.get('description', '')}\nCONTENT:\n{content}"
            documents.append(doc_text)
            metadatas.append({
                "type": "skill",
                "name": name,
                "source": meta['abs_path']
            })
            ids.append(f"skill_{name}")
            print(f"   + Prepared: {name}")
        except Exception as e:
            print(f"   ❌ Error processing {name}: {e}")

    # 3. Upsert
    if documents:
        collection.upsert(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        print(f"✅ Successfully ingested {len(documents)} skills into '{COLLECTION_NAME}'.")
    else:
        print("⚠️ No valid skills to ingest.")

if __name__ == "__main__":
    ingest_skills()
