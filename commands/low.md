---
description: Execute low complexity workflow (quick tasks)
argument-hint: <task-description>
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task, TodoWrite
---

# imlazy Low Complexity Workflow

Execute a low complexity workflow for quick, simple tasks.

## Task
$ARGUMENTS

## Workflow Execution

1. Read the workflow configuration from `${CLAUDE_PLUGIN_ROOT}/.workflow.yaml`
2. Find the `low` workflow definition
3. Execute agents sequentially as defined in the workflow

## Execution Steps

### Step 1: Requirements Analyst
Use the Task tool to launch the `requirements-analyst` agent with:
- The user's task: "$ARGUMENTS"
- Skills to use: requirements-analysis
- Save output to `.imlazy/context/{session}/01-requirements-analyst.md`

### Step 2: Developer
Use the Task tool to launch the `developer` agent with:
- The requirements from Step 1
- Skills to use: implementation
- Save output to `.imlazy/context/{session}/02-developer.md`

## Context Management
- Create session directory: `.imlazy/context/{timestamp}/`
- Each agent saves their output to the context directory
- Pass previous agent's output to the next agent

## Completion
After all agents complete, provide a summary of:
- What was analyzed
- What was implemented
- Any follow-up recommendations
