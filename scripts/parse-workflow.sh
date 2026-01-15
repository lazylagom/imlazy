#!/bin/bash
# imlazy Workflow Parser
# Parses .workflow.yaml and outputs workflow information
#
# Usage:
#   parse-workflow.sh list              - List all workflows
#   parse-workflow.sh get <name>        - Get workflow details as JSON
#   parse-workflow.sh agents <name>     - List agents in a workflow
#   parse-workflow.sh skills <name>     - List all skills in a workflow

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(dirname "$SCRIPT_DIR")}"
WORKFLOW_FILE="${PLUGIN_ROOT}/.workflow.yaml"

# Check if workflow file exists
if [ ! -f "$WORKFLOW_FILE" ]; then
    echo "Error: .workflow.yaml not found at $WORKFLOW_FILE" >&2
    exit 1
fi

# Use Python for YAML parsing (more reliable across systems)
parse_yaml() {
    python3 -c "
import yaml
import json
import sys

with open('$WORKFLOW_FILE', 'r') as f:
    data = yaml.safe_load(f)

query = sys.argv[1] if len(sys.argv) > 1 else ''
if query == 'list':
    workflows = data.get('workflows', {})
    for name in workflows.keys():
        print(name)
elif query.startswith('get:'):
    name = query.split(':')[1]
    workflow = data.get('workflows', {}).get(name)
    if workflow:
        print(json.dumps(workflow, indent=2))
elif query.startswith('agents:'):
    name = query.split(':')[1]
    workflow = data.get('workflows', {}).get(name)
    if workflow:
        for agent in workflow.get('agents', []):
            print(agent.get('name', agent))
elif query.startswith('skills:'):
    name = query.split(':')[1]
    workflow = data.get('workflows', {}).get(name)
    if workflow:
        skills = set()
        for agent in workflow.get('agents', []):
            for skill in agent.get('skills', []):
                skills.add(skill)
        for skill in sorted(skills):
            print(skill)
" "$1"
}

case "${1:-}" in
    list)
        parse_yaml "list"
        ;;
    get)
        if [ -z "${2:-}" ]; then
            echo "Usage: parse-workflow.sh get <workflow-name>" >&2
            exit 1
        fi
        parse_yaml "get:$2"
        ;;
    agents)
        if [ -z "${2:-}" ]; then
            echo "Usage: parse-workflow.sh agents <workflow-name>" >&2
            exit 1
        fi
        parse_yaml "agents:$2"
        ;;
    skills)
        if [ -z "${2:-}" ]; then
            echo "Usage: parse-workflow.sh skills <workflow-name>" >&2
            exit 1
        fi
        parse_yaml "skills:$2"
        ;;
    *)
        echo "Usage: parse-workflow.sh {list|get|agents|skills} [workflow-name]" >&2
        echo ""
        echo "Commands:"
        echo "  list              List all workflow names"
        echo "  get <name>        Get workflow details as JSON"
        echo "  agents <name>     List agents in a workflow"
        echo "  skills <name>     List skills in a workflow"
        exit 1
        ;;
esac
