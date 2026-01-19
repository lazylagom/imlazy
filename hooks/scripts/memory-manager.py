#!/usr/bin/env python3
"""
imlazy 4-Tier Memory Manager

Manages the cognitive memory system:
- Working Memory: Current state (handled by state-manager.py)
- Episodic Memory: Past experiences and problem-solution pairs
- Semantic Memory: Domain knowledge and patterns
- Procedural Memory: Learned methods and strategies

Usage:
  memory-manager.py search TYPE QUERY [--limit N]
  memory-manager.py store TYPE CONTENT [--tags TAG1,TAG2]
  memory-manager.py recall EPISODE_ID
  memory-manager.py consolidate  # Move working to episodic
  memory-manager.py stats
  memory-manager.py prune [--days N]
"""

import json
import os
import sys
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional

IMLAZY_HOME = Path.home() / ".imlazy"
MEMORY_DIRS = {
    "working": IMLAZY_HOME / "working",
    "episodic": IMLAZY_HOME / "episodic",
    "semantic": IMLAZY_HOME / "semantic",
    "procedural": IMLAZY_HOME / "procedural"
}


def ensure_dirs():
    """Ensure all memory directories exist."""
    for path in MEMORY_DIRS.values():
        path.mkdir(parents=True, exist_ok=True)


def generate_id(content: str) -> str:
    """Generate a unique ID for a memory entry."""
    timestamp = datetime.now().isoformat()
    return hashlib.md5(f"{content}{timestamp}".encode()).hexdigest()[:12]


def search_memory(memory_type: str, query: str, limit: int = 5) -> List[Dict]:
    """
    Search memories by type and query.

    Simple keyword matching for now - could be enhanced with embeddings.
    """
    ensure_dirs()

    if memory_type not in MEMORY_DIRS:
        return {"error": f"Invalid memory type: {memory_type}"}

    memory_dir = MEMORY_DIRS[memory_type]
    results = []

    query_lower = query.lower()
    query_terms = query_lower.split()

    for file_path in memory_dir.glob("*.json"):
        try:
            with open(file_path, 'r') as f:
                entry = json.load(f)

            # Score based on keyword matches
            searchable = json.dumps(entry, ensure_ascii=False).lower()
            score = sum(1 for term in query_terms if term in searchable)

            if score > 0:
                results.append({
                    "id": file_path.stem,
                    "score": score,
                    "entry": entry
                })
        except (json.JSONDecodeError, IOError):
            continue

    # Sort by score descending
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:limit]


def store_memory(memory_type: str, content: str, tags: List[str] = None) -> Dict:
    """
    Store a new memory entry.

    For episodic: stores problem-solution pairs
    For semantic: stores patterns and knowledge
    For procedural: stores methods and strategies
    """
    ensure_dirs()

    if memory_type not in MEMORY_DIRS:
        return {"error": f"Invalid memory type: {memory_type}"}

    if memory_type == "working":
        return {"error": "Use state-manager.py for working memory"}

    # Parse content if it's JSON
    try:
        if content.startswith('{') or content.startswith('['):
            content_data = json.loads(content)
        else:
            content_data = {"content": content}
    except json.JSONDecodeError:
        content_data = {"content": content}

    memory_id = generate_id(content)
    entry = {
        "id": memory_id,
        "type": memory_type,
        "data": content_data,
        "tags": tags or [],
        "created_at": datetime.now().isoformat(),
        "access_count": 0,
        "last_accessed": None
    }

    file_path = MEMORY_DIRS[memory_type] / f"{memory_id}.json"
    with open(file_path, 'w') as f:
        json.dump(entry, f, indent=2, ensure_ascii=False)

    return {"success": True, "id": memory_id, "type": memory_type}


def recall_memory(memory_id: str) -> Dict:
    """Recall a specific memory by ID and update access stats."""
    ensure_dirs()

    for memory_type, memory_dir in MEMORY_DIRS.items():
        if memory_type == "working":
            continue

        file_path = memory_dir / f"{memory_id}.json"
        if file_path.exists():
            with open(file_path, 'r') as f:
                entry = json.load(f)

            # Update access stats
            entry["access_count"] = entry.get("access_count", 0) + 1
            entry["last_accessed"] = datetime.now().isoformat()

            with open(file_path, 'w') as f:
                json.dump(entry, f, indent=2, ensure_ascii=False)

            return entry

    return {"error": f"Memory not found: {memory_id}"}


def consolidate_working() -> Dict:
    """
    Consolidate working memory into episodic memory.

    Called when an episode completes successfully.
    Extracts key learnings and stores them.
    """
    ensure_dirs()

    state_file = MEMORY_DIRS["working"] / "state.json"
    if not state_file.exists():
        return {"error": "No working memory to consolidate"}

    with open(state_file, 'r') as f:
        state = json.load(f)

    # Only consolidate if there's meaningful content
    if not state.get("user_query") or not state.get("selected_solution"):
        return {"error": "Working memory incomplete, nothing to consolidate"}

    # Create episodic entry
    episode = {
        "user_query": state["user_query"],
        "problem_reflection": state["problem_reflection"],
        "selected_solution": state["selected_solution"],
        "thought_trace_summary": _summarize_trace(state.get("thought_trace", [])),
        "critiques": state.get("critiques", []),
        "test_results": state.get("test_results", {}),
        "outcome": "success" if not state.get("error_log") else "partial",
        "episode_id": state["episode_id"],
        "project_hash": state["project_hash"]
    }

    result = store_memory("episodic", json.dumps(episode), tags=["episode"])

    # Extract any procedural learnings
    if state.get("critiques"):
        for critique in state["critiques"]:
            if isinstance(critique, dict) and critique.get("correction"):
                store_memory("procedural", json.dumps({
                    "learning": critique["correction"],
                    "context": critique.get("root_cause", ""),
                    "source_episode": state["episode_id"]
                }), tags=["learning", "correction"])

    return {
        "success": True,
        "episodic_id": result["id"],
        "message": "Working memory consolidated to episodic"
    }


def _summarize_trace(trace: List) -> List[str]:
    """Summarize thought trace to key transitions."""
    summary = []
    for item in trace:
        if isinstance(item, dict) and item.get("type") == "transition":
            summary.append(f"{item.get('from', '?')} -> {item.get('to', '?')}")
    return summary[-10:]  # Keep last 10 transitions


def get_stats() -> Dict:
    """Get statistics about the memory system."""
    ensure_dirs()

    stats = {
        "memory_home": str(IMLAZY_HOME),
        "types": {}
    }

    for memory_type, memory_dir in MEMORY_DIRS.items():
        files = list(memory_dir.glob("*.json"))
        total_size = sum(f.stat().st_size for f in files)

        stats["types"][memory_type] = {
            "count": len(files),
            "size_bytes": total_size,
            "size_human": _human_size(total_size)
        }

    return stats


def _human_size(size_bytes: int) -> str:
    """Convert bytes to human readable size."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


def prune_old(days: int = 30) -> Dict:
    """Prune memories older than specified days with zero access."""
    ensure_dirs()

    cutoff = datetime.now() - timedelta(days=days)
    pruned = {"episodic": 0, "semantic": 0, "procedural": 0}

    for memory_type in ["episodic", "semantic", "procedural"]:
        memory_dir = MEMORY_DIRS[memory_type]
        for file_path in memory_dir.glob("*.json"):
            try:
                with open(file_path, 'r') as f:
                    entry = json.load(f)

                created = datetime.fromisoformat(entry.get("created_at", "2000-01-01"))
                access_count = entry.get("access_count", 0)

                # Prune if old and never accessed
                if created < cutoff and access_count == 0:
                    file_path.unlink()
                    pruned[memory_type] += 1
            except (json.JSONDecodeError, IOError, ValueError):
                continue

    return {"pruned": pruned, "cutoff_days": days}


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: memory-manager.py <command> [args]"}))
        sys.exit(1)

    cmd = sys.argv[1].lower()

    try:
        if cmd == "search":
            if len(sys.argv) < 4:
                result = {"error": "Usage: memory-manager.py search TYPE QUERY [--limit N]"}
            else:
                memory_type = sys.argv[2]
                query = sys.argv[3]
                limit = 5
                if "--limit" in sys.argv:
                    idx = sys.argv.index("--limit")
                    if idx + 1 < len(sys.argv):
                        limit = int(sys.argv[idx + 1])
                result = search_memory(memory_type, query, limit)

        elif cmd == "store":
            if len(sys.argv) < 4:
                result = {"error": "Usage: memory-manager.py store TYPE CONTENT [--tags TAG1,TAG2]"}
            else:
                memory_type = sys.argv[2]
                content = sys.argv[3]
                tags = []
                if "--tags" in sys.argv:
                    idx = sys.argv.index("--tags")
                    if idx + 1 < len(sys.argv):
                        tags = sys.argv[idx + 1].split(",")
                result = store_memory(memory_type, content, tags)

        elif cmd == "recall":
            if len(sys.argv) < 3:
                result = {"error": "Usage: memory-manager.py recall MEMORY_ID"}
            else:
                result = recall_memory(sys.argv[2])

        elif cmd == "consolidate":
            result = consolidate_working()

        elif cmd == "stats":
            result = get_stats()

        elif cmd == "prune":
            days = 30
            if "--days" in sys.argv:
                idx = sys.argv.index("--days")
                if idx + 1 < len(sys.argv):
                    days = int(sys.argv[idx + 1])
            result = prune_old(days)

        else:
            result = {"error": f"Unknown command: {cmd}"}

        print(json.dumps(result, indent=2, ensure_ascii=False))

    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
