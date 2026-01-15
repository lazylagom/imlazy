#!/usr/bin/env python3
"""PreToolUse: Validate bash commands before execution"""

import json
import re
import sys

# Dangerous command patterns to block
BLOCKED_PATTERNS = [
    # Destructive file operations
    (r"\brm\s+(-[rf]+\s+)*(/|~|\$HOME|\*)", "rm on root/home/wildcard"),
    (r"\brm\s+-rf\s+\.", "rm -rf in current directory"),
    (r"\bchmod\s+777\b", "chmod 777 (insecure permissions)"),
    (r"\bchown\s+-R\s+.*\s+/", "chown -R on root"),

    # Dangerous git operations
    (r"\bgit\s+push\s+.*--force\b", "git push --force"),
    (r"\bgit\s+push\s+-f\b", "git push -f (force)"),
    (r"\bgit\s+reset\s+--hard\s+origin", "git reset --hard origin"),
    (r"\bgit\s+clean\s+-fd", "git clean -fd (removes untracked files)"),

    # System-level dangers
    (r"\bsudo\s+rm\b", "sudo rm"),
    (r"\bmkfs\b", "mkfs (format disk)"),
    (r"\bdd\s+.*of=/dev/", "dd to device"),
    (r">\s*/dev/sd[a-z]", "write to disk device"),
    (r"\bshutdown\b", "shutdown command"),
    (r"\breboot\b", "reboot command"),

    # Network dangers
    (r"\bcurl\s+.*\|\s*(ba)?sh", "curl pipe to shell"),
    (r"\bwget\s+.*\|\s*(ba)?sh", "wget pipe to shell"),

    # Fork bomb / resource exhaustion
    (r":\(\)\s*\{\s*:\|:&\s*\}\s*;:", "fork bomb"),
    (r"\bwhile\s+true.*done", "infinite loop"),
]

# Warning patterns (allow but warn)
WARNING_PATTERNS = [
    (r"\brm\s+-rf?\b", "rm with force flag - verify target"),
    (r"\bgit\s+stash\s+drop", "git stash drop - data loss possible"),
    (r"\bnpm\s+cache\s+clean", "npm cache clean"),
]

def validate_command(command: str) -> tuple[bool, str]:
    """Validate command against patterns. Returns (blocked, message)."""
    command_lower = command.lower()

    # Check blocked patterns
    for pattern, description in BLOCKED_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            return True, f"Blocked: {description}"

    # Check warning patterns (not blocked, just warn)
    warnings = []
    for pattern, description in WARNING_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            warnings.append(description)

    if warnings:
        print(f"Warning: {', '.join(warnings)}", file=sys.stderr)

    return False, ""

def main():
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}", file=sys.stderr)
        sys.exit(1)

    tool_name = input_data.get("tool_name", "")
    if tool_name != "Bash":
        sys.exit(0)

    command = input_data.get("tool_input", {}).get("command", "")
    if not command:
        sys.exit(0)

    blocked, message = validate_command(command)

    if blocked:
        print(f"Command blocked: {message}", file=sys.stderr)
        print(f"Command was: {command[:100]}...", file=sys.stderr)
        sys.exit(2)  # Exit code 2 = block

    sys.exit(0)

if __name__ == "__main__":
    main()
