#!/usr/bin/env python3
"""
imlazy Workflow Logger

Unified logging for Agent, Command, Skill, and Hook execution.
Outputs to both file (JSON Lines) and console (colored).

Usage:
  workflow-logger.py --type TYPE --name NAME --event EVENT [--meta JSON] [--stdin]

Arguments:
  --type   : AGENT, COMMAND, SKILL, HOOK
  --name   : Component name (e.g., planner, bash-validator)
  --event  : START, END, ERROR, PASS, FAIL
  --meta   : JSON string with additional metadata
  --stdin  : Read hook context from stdin

Examples:
  workflow-logger.py --type AGENT --name planner --event START
  workflow-logger.py --type HOOK --name bash-validator --event PASS
  workflow-logger.py --type AGENT --name coder --event END --meta '{"duration": 4.2}'
"""

import json
import os
import sys
import argparse
from datetime import datetime
from pathlib import Path

# Paths
IMLAZY_HOME = Path.home() / ".imlazy"
LOGS_DIR = IMLAZY_HOME / "logs"
LOG_FILE = LOGS_DIR / "workflow.log"

# ANSI Colors
COLORS = {
    "reset": "\033[0m",
    "bold": "\033[1m",
    "dim": "\033[2m",
    # Event colors
    "green": "\033[32m",  # START, PASS
    "blue": "\033[34m",  # END
    "red": "\033[31m",  # ERROR, FAIL
    "yellow": "\033[33m",  # WARNING
    "cyan": "\033[36m",  # INFO
    "magenta": "\033[35m",  # SKILL
    # Type colors
    "agent": "\033[38;5;208m",  # Orange
    "command": "\033[38;5;141m",  # Purple
    "skill": "\033[38;5;205m",  # Pink
    "hook": "\033[38;5;75m",  # Light blue
}

# Event icons
ICONS = {
    "START": "🟢",
    "END": "🔵",
    "ERROR": "🔴",
    "PASS": "✅",
    "FAIL": "❌",
    "INFO": "ℹ️",
}

# Event colors
EVENT_COLORS = {
    "START": "green",
    "END": "blue",
    "ERROR": "red",
    "PASS": "green",
    "FAIL": "red",
    "INFO": "cyan",
}


def ensure_log_dir():
    """Ensure log directory exists."""
    LOGS_DIR.mkdir(parents=True, exist_ok=True)


def format_console(log_type: str, name: str, event: str, meta: dict = None) -> str:
    """Format log entry for console with colors."""
    icon = ICONS.get(event, "📌")
    type_color = COLORS.get(log_type.lower(), COLORS["cyan"])
    event_color = COLORS.get(EVENT_COLORS.get(event, "cyan"), COLORS["cyan"])
    reset = COLORS["reset"]
    dim = COLORS["dim"]

    # Main line
    line = f"{icon} {type_color}[{log_type}:{name}]{reset} {event_color}{event}{reset}"

    # Add metadata details
    if meta:
        # Duration
        if "duration" in meta:
            line += f" {dim}({meta['duration']:.1f}s){reset}"

        # Status
        if "status" in meta:
            status = meta["status"]
            status_color = COLORS["green"] if status == "success" else COLORS["red"]
            line += f" {status_color}{status}{reset}"

        # Task description (for agents)
        if "task" in meta:
            task = (
                meta["task"][:50] + "..."
                if len(meta.get("task", "")) > 50
                else meta.get("task", "")
            )
            line += f'\n   └─ {dim}task: "{task}"{reset}'

        # Error message
        if "error" in meta:
            error = (
                meta["error"][:80] + "..."
                if len(meta.get("error", "")) > 80
                else meta.get("error", "")
            )
            line += f"\n   └─ {COLORS['red']}error: {error}{reset}"

        # Reason (for hook decisions)
        if "reason" in meta:
            line += f"\n   └─ {dim}reason: {meta['reason']}{reset}"

    return line


def format_file(log_type: str, name: str, event: str, meta: dict = None) -> str:
    """Format log entry for file as JSON Line."""
    entry = {
        "ts": datetime.now().isoformat(),
        "type": log_type,
        "name": name,
        "event": event,
    }
    if meta:
        entry["meta"] = meta

    return json.dumps(entry, ensure_ascii=False)


def log(
    log_type: str,
    name: str,
    event: str,
    meta: dict = None,
    to_console: bool = True,
    to_file: bool = True,
):
    """
    Write log entry to console and/or file.

    Args:
        log_type: AGENT, COMMAND, SKILL, HOOK
        name: Component name
        event: START, END, ERROR, PASS, FAIL
        meta: Additional metadata dict
        to_console: Output to stderr
        to_file: Append to log file
    """
    ensure_log_dir()

    # Console output (stderr so it doesn't interfere with hook JSON output)
    if to_console:
        console_line = format_console(log_type, name, event, meta)
        print(console_line, file=sys.stderr)

    # File output (JSON Lines format)
    if to_file:
        file_line = format_file(log_type, name, event, meta)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(file_line + "\n")


def init_log():
    """Initialize log file for new session."""
    ensure_log_dir()

    # Create session marker
    session_entry = {
        "ts": datetime.now().isoformat(),
        "type": "SESSION",
        "name": "imlazy",
        "event": "START",
        "meta": {
            "cwd": os.getcwd(),
            "log_file": str(LOG_FILE),
        },
    }

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(session_entry, ensure_ascii=False) + "\n")

    return session_entry


def parse_hook_context():
    """Parse hook context from stdin if available."""
    if not sys.stdin.isatty():
        try:
            stdin_data = sys.stdin.read()
            if stdin_data.strip():
                return json.loads(stdin_data)
        except (json.JSONDecodeError, IOError):
            pass
    return None


def extract_agent_info(hook_context: dict) -> dict:
    """Extract agent information from hook context."""
    meta = {}

    if not hook_context:
        return meta

    tool_input = hook_context.get("tool_input", {})
    tool_result = hook_context.get("tool_result", {})

    # For Task tool (agent invocation)
    if "subagent_type" in tool_input:
        meta["subagent_type"] = tool_input["subagent_type"]

    if "description" in tool_input:
        meta["task"] = tool_input["description"]

    if "prompt" in tool_input:
        # Truncate long prompts
        prompt = tool_input["prompt"]
        meta["prompt_preview"] = prompt[:100] + "..." if len(prompt) > 100 else prompt

    # For tool results
    if isinstance(tool_result, dict):
        if "error" in tool_result:
            meta["error"] = tool_result["error"]
        if "duration" in tool_result:
            meta["duration"] = tool_result["duration"]

    return meta


def main():
    parser = argparse.ArgumentParser(description="imlazy Workflow Logger")
    parser.add_argument(
        "--type",
        required=True,
        choices=["AGENT", "COMMAND", "SKILL", "HOOK", "SESSION"],
        help="Log entry type",
    )
    parser.add_argument("--name", required=True, help="Component name")
    parser.add_argument(
        "--event",
        required=True,
        choices=["START", "END", "ERROR", "PASS", "FAIL", "INFO"],
        help="Event type",
    )
    parser.add_argument("--meta", help="JSON metadata string")
    parser.add_argument(
        "--stdin", action="store_true", help="Read hook context from stdin"
    )
    parser.add_argument(
        "--init", action="store_true", help="Initialize log for new session"
    )
    parser.add_argument("--no-console", action="store_true", help="Skip console output")
    parser.add_argument("--no-file", action="store_true", help="Skip file output")

    args = parser.parse_args()

    # Initialize mode
    if args.init:
        result = init_log()
        print(json.dumps(result))
        return

    # Parse metadata
    meta = {}
    if args.meta:
        try:
            meta = json.loads(args.meta)
        except json.JSONDecodeError:
            meta = {"raw": args.meta}

    # Parse hook context from stdin
    if args.stdin:
        hook_context = parse_hook_context()
        if hook_context:
            agent_info = extract_agent_info(hook_context)
            meta.update(agent_info)

    # Write log
    log(
        log_type=args.type,
        name=args.name,
        event=args.event,
        meta=meta if meta else None,
        to_console=not args.no_console,
        to_file=not args.no_file,
    )


if __name__ == "__main__":
    main()
