"""
ResearchProAI — LLM Report Generator
======================================
Queries the ChromaDB knowledge base and generates structured
reports using Groq (Llama-3.3-70b).

Usage:
    python src/generate_report.py "What are the best ensemble strategies?"
"""
import os
import sys
import chromadb
from chromadb.utils import embedding_functions
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# ─── Configuration ───────────────────────────────────────────────
DB_DIR = "chroma_db"
COLLECTION_NAME = "knowledge_base"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
LLM_MODEL = "llama-3.3-70b-versatile"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


import re

def sanitize_input(text):
    """Sanitize input using a robust whitelist approach to prevent injection."""
    if not isinstance(text, str):
        return ""
    # Allow: alphanumeric, whitespace, common punctuation. Filter out control characters.
    # Specifically blocks: ; ` $ | & < > \
    sanitized = re.sub(r'[;`$|&<>\\]', '', text)
    return sanitized.strip()


def get_context(query, n_results=40):
    """Retrieve relevant chunks with filename-based metadata filtering for high precision."""
    client = chromadb.PersistentClient(path=DB_DIR)
    ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL)
    collection = client.get_collection(name=COLLECTION_NAME, embedding_function=ef)
    
    safe_query = sanitize_input(query).lower()
    
    # Precise keyword filtering (e.g., s6e3)
    filter_keywords = [word for word in ["s6e3", "churn", "tabnet"] if word in safe_query]
    
    # If a specific competition ID is found, use it as a metadata filter to guarantee retrieval
    where_filter = None
    if filter_keywords:
        # We look for the keyword anywhere in the source path
        where_filter = {"source": {"$contains": filter_keywords[0]}}
    
    try:
        results = collection.query(
            query_texts=[safe_query], 
            n_results=n_results,
            where=where_filter
        )
    except Exception:
        # Fallback to no filter if where clause fails
        results = collection.query(query_texts=[safe_query], n_results=n_results)
    
    context_parts = []
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        source = meta.get("source", "Unknown")
        context_parts.append(f"--- SOURCE: {os.path.basename(source)} ---\n{doc}")
        
    return "\n\n".join(context_parts)[:40000] # Increased context window for Gemini

import google.generativeai as genai
from mistralai import Mistral

def generate_report(query):
    """Generate an LLM report with automatic key rotation and provider fallback."""
    # ─── API Key Collection ───────────────────────────────────────────────
    gemini_keys = [
        os.getenv("GEMINI_KEY_1"),
        os.getenv("GEMINI_KEY_2"),
        os.getenv("GEMINI_KEY_3"),
        os.getenv("GEMINI_KEY_4"),
        os.getenv("GEMINI_API_KEY")
    ]
    gemini_keys = [k for k in gemini_keys if k] # Filter out None
    mistral_key = os.getenv("MISTRAL_API_KEY")

    print(f"🔍 Searching knowledge base for: '{query}'...")
    context = get_context(query, n_results=40)

    import re
    sources = list(set(re.findall(r"--- SOURCE: (.*?) ---", context)))
    print(f"📄 Sources found: {sources}")

    system_instruction = (
        "You are ResearchPro AI, a world-class Kaggle Grandmaster and Python Engineer. "
        "Your goal is to extract EXACT feature engineering kod, kolone i "
        "ensemble težine iz dostavljenog konteksta. "
        "Ako vidiš kod, citiraj ga tačno. Odgovori na srpskom jeziku."
    )
    
    prompt = (
        f"{system_instruction}\n\n"
        f"Dostavljeni kontekst iz baze znanja (Notebooks & Solutions):\n"
        f"{context}\n\n"
        f"Korisničko pitanje: {query}\n\n"
        f"Pronađi tačan kod za transformacije i prioritizuj s6e3 podatke."
    )

    # ─── Phase 1: Try Gemini with Rotation ────────────────────────────────
    for i, api_key in enumerate(gemini_keys):
        print(f"🤖 Generating with Gemini (Key #{i+1})...")
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            err_msg = str(e)
            if "429" in err_msg or "quota" in err_msg.lower():
                print(f"  ⚠️ Key #{i+1} Quota Exceeded. Rotating...")
                continue
            else:
                print(f"  ❌ Gemini Error: {err_msg}")
                break # Non-quota error, try fallback

    # ─── Phase 2: Fallback to Mistral ──────────────────────────────────────
    if mistral_key:
        print(f"🤖 Gemini Failed or Quota Exceeded. Falling back to Mistral (Pixtral-Large)...")
        try:
            client = Mistral(api_key=mistral_key)
            # Using large model for best quality logic
            response = client.chat.complete(
                model="pixtral-large-latest",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"❌ All providers failed. Final error (Mistral): {str(e)}"
    
    return "❌ All providers failed and no Mistral key found."

if __name__ == "__main__":
    q = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Perform a general audit of this project."
    report = generate_report(q)
    print("\n" + "=" * 50)
    print(report)
    print("=" * 50)
