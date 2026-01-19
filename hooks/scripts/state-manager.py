#!/usr/bin/env python3
"""
imlazy CognitiveState Manager

Manages the working memory state for the cognitive agent workflow.
Provides CRUD operations for CognitiveState JSON.

Usage:
  state-manager.py init [--project-hash HASH]
  state-manager.py get [KEY]
  state-manager.py set KEY VALUE
  state-manager.py update KEY VALUE  # For appending to lists
  state-manager.py transition NODE
  state-manager.py reset
  state-manager.py dump
"""

import json
import os
import sys
import uuid
import hashlib
from datetime import datetime
from pathlib import Path

IMLAZY_HOME = Path.home() / ".imlazy"
WORKING_DIR = IMLAZY_HOME / "working"
STATE_FILE = WORKING_DIR / "state.json"

DEFAULT_STATE = {
    # Task
    "user_query": "",
    "problem_reflection": {
        "goal": "",
        "inputs": [],
        "outputs": [],
        "constraints": [],
        "edge_cases": []
    },

    # Thought process
    "current_plan": [],
    "thought_trace": [],
    "critiques": [],
    "possible_solutions": [],
    "selected_solution": "",

    # Execution context
    "file_context": {},
    "test_results": {
        "public_tests": [],
        "ai_tests": [],
        "anchor_tests": []
    },
    "error_log": [],

    # Cycle control
    "current_node": "PLANNER",
    "retry_count": 0,
    "max_retries": 3,

    # Meta
    "episode_id": "",
    "project_hash": "",
    "created_at": "",
    "updated_at": ""
}

VALID_NODES = ["PLANNER", "REASONER", "CODER", "VERIFIER", "REFLECTOR", "CONSOLIDATOR"]


def ensure_dirs():
    """Ensure imlazy directories exist."""
    WORKING_DIR.mkdir(parents=True, exist_ok=True)
    (IMLAZY_HOME / "episodic").mkdir(exist_ok=True)
    (IMLAZY_HOME / "semantic").mkdir(exist_ok=True)
    (IMLAZY_HOME / "procedural").mkdir(exist_ok=True)


def get_project_hash(project_path=None):
    """Generate a hash for the current project."""
    if project_path is None:
        project_path = os.getcwd()
    return hashlib.md5(project_path.encode()).hexdigest()[:8]


def load_state():
    """Load current state from file."""
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return None


def save_state(state):
    """Save state to file."""
    ensure_dirs()
    state["updated_at"] = datetime.now().isoformat()
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def init_state(project_hash=None):
    """Initialize a new cognitive state."""
    ensure_dirs()

    state = DEFAULT_STATE.copy()
    state["problem_reflection"] = DEFAULT_STATE["problem_reflection"].copy()
    state["test_results"] = {k: list(v) for k, v in DEFAULT_STATE["test_results"].items()}

    state["episode_id"] = str(uuid.uuid4())[:8]
    state["project_hash"] = project_hash or get_project_hash()
    state["created_at"] = datetime.now().isoformat()
    state["updated_at"] = state["created_at"]

    save_state(state)
    return state


def get_value(key=None):
    """Get a value from state."""
    state = load_state()
    if state is None:
        return {"error": "No active state. Run 'init' first."}

    if key is None:
        return state

    # Support nested keys like "problem_reflection.goal"
    keys = key.split(".")
    value = state
    for k in keys:
        if isinstance(value, dict) and k in value:
            value = value[k]
        else:
            return {"error": f"Key not found: {key}"}

    return {"key": key, "value": value}


def set_value(key, value):
    """Set a value in state."""
    state = load_state()
    if state is None:
        return {"error": "No active state. Run 'init' first."}

    # Parse JSON value if it looks like JSON
    if isinstance(value, str):
        try:
            if value.startswith('[') or value.startswith('{'):
                value = json.loads(value)
        except json.JSONDecodeError:
            pass

    # Support nested keys
    keys = key.split(".")
    target = state
    for k in keys[:-1]:
        if k not in target:
            target[k] = {}
        target = target[k]

    target[keys[-1]] = value
    save_state(state)
    return {"success": True, "key": key, "value": value}


def update_value(key, value):
    """Append a value to a list in state."""
    state = load_state()
    if state is None:
        return {"error": "No active state. Run 'init' first."}

    # Parse JSON value if it looks like JSON
    if isinstance(value, str):
        try:
            if value.startswith('[') or value.startswith('{'):
                value = json.loads(value)
        except json.JSONDecodeError:
            pass

    # Support nested keys
    keys = key.split(".")
    target = state
    for k in keys[:-1]:
        if k not in target:
            target[k] = {}
        target = target[k]

    final_key = keys[-1]
    if final_key not in target:
        target[final_key] = []

    if not isinstance(target[final_key], list):
        return {"error": f"Key {key} is not a list"}

    target[final_key].append(value)
    save_state(state)
    return {"success": True, "key": key, "appended": value}


def transition_node(node):
    """Transition to a new node in the workflow."""
    state = load_state()
    if state is None:
        return {"error": "No active state. Run 'init' first."}

    node = node.upper()
    if node not in VALID_NODES:
        return {"error": f"Invalid node: {node}. Valid: {VALID_NODES}"}

    prev_node = state["current_node"]
    state["current_node"] = node

    # Record transition in thought trace
    transition = {
        "type": "transition",
        "from": prev_node,
        "to": node,
        "timestamp": datetime.now().isoformat()
    }
    state["thought_trace"].append(transition)

    save_state(state)
    return {"success": True, "from": prev_node, "to": node}


def reset_state():
    """Reset state for a new episode while preserving project context."""
    state = load_state()
    project_hash = state["project_hash"] if state else get_project_hash()
    return init_state(project_hash)


def dump_state():
    """Dump current state as formatted JSON."""
    state = load_state()
    if state is None:
        return {"error": "No active state"}
    return state


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: state-manager.py <command> [args]"}))
        sys.exit(1)

    cmd = sys.argv[1].lower()

    try:
        if cmd == "init":
            project_hash = None
            if len(sys.argv) > 3 and sys.argv[2] == "--project-hash":
                project_hash = sys.argv[3]
            result = init_state(project_hash)
        elif cmd == "get":
            key = sys.argv[2] if len(sys.argv) > 2 else None
            result = get_value(key)
        elif cmd == "set":
            if len(sys.argv) < 4:
                result = {"error": "Usage: state-manager.py set KEY VALUE"}
            else:
                result = set_value(sys.argv[2], sys.argv[3])
        elif cmd == "update":
            if len(sys.argv) < 4:
                result = {"error": "Usage: state-manager.py update KEY VALUE"}
            else:
                result = update_value(sys.argv[2], sys.argv[3])
        elif cmd == "transition":
            if len(sys.argv) < 3:
                result = {"error": "Usage: state-manager.py transition NODE"}
            else:
                result = transition_node(sys.argv[2])
        elif cmd == "reset":
            result = reset_state()
        elif cmd == "dump":
            result = dump_state()
        else:
            result = {"error": f"Unknown command: {cmd}"}

        print(json.dumps(result, indent=2, ensure_ascii=False))

    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
