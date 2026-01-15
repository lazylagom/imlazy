#!/usr/bin/env python3
"""PreToolUse: Protect sensitive files from being edited/written"""

import json
import os
import re
import sys

# Protected file patterns
PROTECTED_PATTERNS = [
    # Environment and secrets
    r"\.env$",
    r"\.env\.[a-z]+$",  # .env.local, .env.production, etc.
    r"\.secret",
    r"credentials\.json$",
    r"secrets\.ya?ml$",
    r"\.pem$",
    r"\.key$",
    r"id_rsa",
    r"id_ed25519",

    # Lock files (usually auto-generated)
    r"package-lock\.json$",
    r"yarn\.lock$",
    r"pnpm-lock\.yaml$",
    r"Gemfile\.lock$",
    r"poetry\.lock$",
    r"Cargo\.lock$",
    r"composer\.lock$",

    # Git internals
    r"\.git/",
    r"\.gitattributes$",

    # IDE/Editor config (usually personal)
    r"\.idea/",
    r"\.vscode/settings\.json$",

    # Database files
    r"\.sqlite$",
    r"\.db$",
]

# Files that trigger a warning but are allowed
WARNING_PATTERNS = [
    (r"\.gitignore$", "Modifying .gitignore"),
    (r"tsconfig\.json$", "Modifying TypeScript config"),
    (r"package\.json$", "Modifying package.json"),
]

def is_protected(file_path: str) -> tuple[bool, str]:
    """Check if file is protected. Returns (protected, pattern_matched)."""
    # Normalize path
    normalized = os.path.normpath(file_path)

    for pattern in PROTECTED_PATTERNS:
        if re.search(pattern, normalized, re.IGNORECASE):
            return True, pattern

    return False, ""

def check_warnings(file_path: str) -> list[str]:
    """Return list of warnings for the file."""
    warnings = []
    for pattern, message in WARNING_PATTERNS:
        if re.search(pattern, file_path, re.IGNORECASE):
            warnings.append(message)
    return warnings

def main():
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}", file=sys.stderr)
        sys.exit(1)

    tool_name = input_data.get("tool_name", "")
    if tool_name not in ("Edit", "Write"):
        sys.exit(0)

    file_path = input_data.get("tool_input", {}).get("file_path", "")
    if not file_path:
        sys.exit(0)

    # Check if protected
    protected, pattern = is_protected(file_path)
    if protected:
        print(f"Protected file: {file_path}", file=sys.stderr)
        print(f"Matched pattern: {pattern}", file=sys.stderr)
        print("This file type is protected from automatic edits.", file=sys.stderr)
        sys.exit(2)  # Block

    # Check for warnings
    warnings = check_warnings(file_path)
    for warning in warnings:
        print(f"Warning: {warning}", file=sys.stderr)

    sys.exit(0)

if __name__ == "__main__":
    main()
