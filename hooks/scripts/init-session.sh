#!/bin/bash
# imlazy Session Initialization Hook
# Creates the context directory structure for workflow execution

set -euo pipefail

# Get project directory from environment
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"

# Create .imlazy directory structure
IMLAZY_DIR="${PROJECT_DIR}/.imlazy"
CONTEXT_DIR="${IMLAZY_DIR}/context"

# Create directories if they don't exist
mkdir -p "${CONTEXT_DIR}"

# Check if .workflow.yaml exists
WORKFLOW_FILE="${CLAUDE_PLUGIN_ROOT}/.workflow.yaml"
if [ -f "${WORKFLOW_FILE}" ]; then
    # Output system message to inform Claude about imlazy availability
    echo '{"systemMessage": "imlazy workflow system initialized. Available commands: /imlazy:on, /imlazy:low, /imlazy:medium, /imlazy:high, /imlazy:create-workflow"}'
else
    echo '{"systemMessage": "imlazy plugin loaded but .workflow.yaml not found. Run /imlazy:create-workflow to create one."}'
fi

exit 0
