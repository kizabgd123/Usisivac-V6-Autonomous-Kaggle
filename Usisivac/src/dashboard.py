"""
ResearchProAI — Knowledge Dashboard
=====================================
Live CLI dashboard showing the health and saturation of your
ChromaDB knowledge base and agent audit collections.

Usage:
    python src/dashboard.py
"""
import os
import time
from datetime import datetime
import chromadb

# ─── Configuration ───────────────────────────────────────────────
DB_DIR = "chroma_db"
KB_COLLECTION = "knowledge_base"
AUDIT_COLLECTION = "agent_history"
TARGET_CHUNKS = 10_000  # Adjust to your goal


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def get_stats():
    """Read collection counts from ChromaDB."""
    try:
        client = chromadb.PersistentClient(path=DB_DIR)
        collections = {c.name: c.count() for c in client.list_collections()}
        return collections
    except Exception:
        return {}


def draw(collections):
    """Render the dashboard."""
    clear()
    kb = collections.get(KB_COLLECTION, 0)
    audit = collections.get(AUDIT_COLLECTION, 0)
    progress = min((kb / TARGET_CHUNKS) * 100, 100) if TARGET_CHUNKS > 0 else 0
    bar_len = 25
    filled = int(bar_len * progress / 100)
    bar = "█" * filled + "─" * (bar_len - filled)

    print("╔══════════════════════════════════════════════════╗")
    print("║   🏛️  RESEARCH PRO AI — KNOWLEDGE DASHBOARD      ║")
    print("╠══════════════════════════════════════════════════╣")
    print(f"║  ⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}                        ║")
    print("╠══════════════════════════════════════════════════╣")
    print(f"║  📂 Knowledge Base:  {kb:>8,} chunks               ║")
    print(f"║  🕵️  Agent Audit:     {audit:>8,} fragments            ║")
    print(f"║  📊 Saturation:      [{bar}] {progress:>5.1f}%  ║")
    print("╠══════════════════════════════════════════════════╣")

    # Show all collections
    for name, count in sorted(collections.items()):
        if name not in (KB_COLLECTION, AUDIT_COLLECTION):
            print(f"║  📦 {name:<20s} {count:>8,} items          ║")

    print("╠══════════════════════════════════════════════════╣")
    print("║  Refreshing every 10s — Press Ctrl+C to exit    ║")
    print("╚══════════════════════════════════════════════════╝")


def main():
    while True:
        stats = get_stats()
        draw(stats)
        try:
            time.sleep(10)
        except KeyboardInterrupt:
            print("\n👋 Dashboard closed.")
            break


if __name__ == "__main__":
    main()
