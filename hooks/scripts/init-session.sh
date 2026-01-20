#!/bin/bash
# imlazy Session Initialization Hook

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
IMLAZY_HOME="${HOME}/.imlazy"
LOGS_DIR="${IMLAZY_HOME}/logs"

# Ensure log directory exists
mkdir -p "${LOGS_DIR}"

# Initialize workflow log for this session
python3 "${SCRIPT_DIR}/workflow-logger.py" --type SESSION --name imlazy --event START --meta "{\"cwd\": \"$(pwd)\"}" --no-console 2>/dev/null

echo '{"systemMessage": "imlazy ready. Commands: /imlazy:think, /imlazy:memory, /imlazy:state, /imlazy:doctor | Modes: /imlazy:orient, /imlazy:explore, /imlazy:theorize, /imlazy:execute, /imlazy:verify"}'
exit 0
