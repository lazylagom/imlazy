#!/bin/bash
# PostToolUse: Auto-format files after Edit/Write

# Read JSON input from stdin
INPUT=$(cat)

# Extract file path
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

if [ -z "$FILE_PATH" ] || [ ! -f "$FILE_PATH" ]; then
    exit 0
fi

# Get file extension
EXT="${FILE_PATH##*.}"

# Format based on file type
case "$EXT" in
    js|jsx|ts|tsx|json|css|scss|md|html|yaml|yml)
        if command -v prettier &> /dev/null; then
            prettier --write "$FILE_PATH" 2>/dev/null && echo "Formatted: $FILE_PATH"
        elif command -v npx &> /dev/null; then
            npx prettier --write "$FILE_PATH" 2>/dev/null && echo "Formatted: $FILE_PATH"
        fi
        ;;
    py)
        if command -v black &> /dev/null; then
            black -q "$FILE_PATH" 2>/dev/null && echo "Formatted: $FILE_PATH"
        elif command -v ruff &> /dev/null; then
            ruff format "$FILE_PATH" 2>/dev/null && echo "Formatted: $FILE_PATH"
        fi
        ;;
    go)
        if command -v gofmt &> /dev/null; then
            gofmt -w "$FILE_PATH" 2>/dev/null && echo "Formatted: $FILE_PATH"
        fi
        ;;
    rs)
        if command -v rustfmt &> /dev/null; then
            rustfmt "$FILE_PATH" 2>/dev/null && echo "Formatted: $FILE_PATH"
        fi
        ;;
esac

exit 0
