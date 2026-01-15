#!/bin/bash
# imlazy Workflow Detection Hook
# Detects when imlazy workflow commands are being used and provides context

set -euo pipefail

# Read input from stdin
input=$(cat)

# Extract user prompt
user_prompt=$(echo "$input" | jq -r '.user_prompt // ""')

# Check if this is an imlazy command
if [[ "$user_prompt" =~ ^/imlazy ]]; then
    # Get project directory
    PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"

    # Create session ID based on timestamp
    SESSION_ID=$(date +%Y%m%d_%H%M%S)
    SESSION_DIR="${PROJECT_DIR}/.imlazy/context/${SESSION_ID}"

    # Create session directory
    mkdir -p "${SESSION_DIR}"

    # Provide workflow context to Claude
    WORKFLOW_FILE="${CLAUDE_PLUGIN_ROOT}/.workflow.yaml"

    if [ -f "${WORKFLOW_FILE}" ]; then
        # Read workflow file content for context
        workflow_content=$(cat "${WORKFLOW_FILE}")

        # Output system message with workflow context
        cat << EOF
{
    "systemMessage": "imlazy workflow session started. Session ID: ${SESSION_ID}. Context directory: ${SESSION_DIR}. When executing agents, save each agent's output to this directory with numbered prefixes (e.g., 01-requirements-analyst.md). Pass previous agent outputs as context to subsequent agents."
}
EOF
    else
        echo '{"systemMessage": "Warning: .workflow.yaml not found. Please ensure the workflow configuration exists."}'
    fi
fi

exit 0
