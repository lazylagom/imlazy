#!/usr/bin/env python3
"""
imlazy Reflection Trigger Hook

Automatically triggers REFLECTOR when test failures are detected.
Runs as a PostToolUse hook after Bash commands.

Usage (in hooks.json):
  {
    "matcher": "Bash",
    "hooks": [{
      "type": "command",
      "command": "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/reflection-trigger.py"
    }]
  }
"""

import json
import os
import sys
from pathlib import Path

IMLAZY_HOME = Path.home() / ".imlazy"
STATE_FILE = IMLAZY_HOME / "working" / "state.json"

# Patterns that indicate test failures
FAILURE_PATTERNS = [
    "FAILED",
    "FAIL:",
    "Error:",
    "AssertionError",
    "TypeError",
    "SyntaxError",
    "ReferenceError",
    "test failed",
    "tests failed",
    "npm ERR!",
    "pytest: error",
    "FAILURES",
    "panic:",
    "error[E",
]

# Patterns that indicate success (to avoid false positives)
SUCCESS_PATTERNS = [
    "All tests passed",
    "passed",
    "0 failed",
    "OK",
    "PASSED",
]


def load_state():
    """Load current cognitive state."""
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return None


def save_state(state):
    """Save cognitive state."""
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def check_for_failures(output: str) -> bool:
    """Check if output contains test failure patterns."""
    output_lower = output.lower()

    # Check for success patterns first
    for pattern in SUCCESS_PATTERNS:
        if pattern.lower() in output_lower:
            # If we see success indicators, be more careful about failures
            pass

    # Check for failure patterns
    for pattern in FAILURE_PATTERNS:
        if pattern.lower() in output_lower:
            return True

    return False


def should_trigger_reflection(state: dict, tool_result: str) -> dict:
    """Determine if reflection should be triggered."""
    current_node = state.get("current_node", "")

    # Only trigger during CODER or VERIFIER nodes
    if current_node not in ["CODER", "VERIFIER"]:
        return {"trigger": False, "reason": f"Not in CODER/VERIFIER (currently {current_node})"}

    # Check for failures in output
    if check_for_failures(tool_result):
        return {
            "trigger": True,
            "reason": "Test failure detected",
            "failure_type": "test_failure"
        }

    return {"trigger": False, "reason": "No failures detected"}


def record_failure(state: dict, failure_info: dict, tool_result: str):
    """Record failure to state for REFLECTOR."""
    error_entry = {
        "type": failure_info.get("failure_type", "unknown"),
        "trigger": "automatic",
        "output_snippet": tool_result[:500] if len(tool_result) > 500 else tool_result,
        "from_node": state.get("current_node", "unknown")
    }

    if "error_log" not in state:
        state["error_log"] = []

    state["error_log"].append(error_entry)
    save_state(state)


def main():
    # Read tool result from stdin (passed by hook system)
    tool_result = ""
    if not sys.stdin.isatty():
        tool_result = sys.stdin.read()

    # Also check environment for tool output
    tool_output_env = os.environ.get("CLAUDE_TOOL_OUTPUT", "")
    if tool_output_env:
        tool_result = tool_output_env

    if not tool_result:
        # No output to analyze
        print(json.dumps({"status": "skip", "reason": "No tool output"}))
        return

    state = load_state()
    if not state:
        # No active cognitive state
        print(json.dumps({"status": "skip", "reason": "No active state"}))
        return

    result = should_trigger_reflection(state, tool_result)

    if result["trigger"]:
        # Record the failure
        record_failure(state, result, tool_result)

        # Output recommendation (the orchestrator should handle the actual transition)
        print(json.dumps({
            "status": "failure_detected",
            "recommendation": "REFLECTOR",
            "reason": result["reason"],
            "message": "Test failure detected. Consider transitioning to REFLECTOR for analysis."
        }))
    else:
        print(json.dumps({
            "status": "ok",
            "reason": result["reason"]
        }))


if __name__ == "__main__":
    main()
