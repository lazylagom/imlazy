---
description: Execute medium complexity workflow (standard tasks)
argument-hint: <task-description>
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task, TodoWrite
---

# imlazy Medium Complexity Workflow

Execute a medium complexity workflow for standard development tasks.

## Task
$ARGUMENTS

## Workflow Execution

1. Read the workflow configuration from `${CLAUDE_PLUGIN_ROOT}/.workflow.yaml`
2. Find the `medium` workflow definition
3. Execute agents sequentially as defined in the workflow

## Execution Steps

### Step 1: Requirements Analyst
Use the Task tool to launch the `requirements-analyst` agent with:
- The user's task: "$ARGUMENTS"
- Skills to use: requirements-analysis
- Save output to `.imlazy/context/{session}/01-requirements-analyst.md`

### Step 2: Code Analyst
Use the Task tool to launch the `code-analyst` agent with:
- The requirements from Step 1
- Skills to use: code-analysis
- Save output to `.imlazy/context/{session}/02-code-analyst.md`

### Step 3: Developer
Use the Task tool to launch the `developer` agent with:
- The requirements and code analysis from previous steps
- Skills to use: implementation
- Save output to `.imlazy/context/{session}/03-developer.md`

### Step 4: Reviewer
Use the Task tool to launch the `reviewer` agent with:
- All previous context
- Skills to use: code-review
- Save output to `.imlazy/context/{session}/04-reviewer.md`

## Context Management
- Create session directory: `.imlazy/context/{timestamp}/`
- Each agent saves their output to the context directory
- Pass previous agent's output to the next agent

## Completion
After all agents complete, provide a summary of:
- Requirements analyzed
- Code analysis findings
- Implementation details
- Review feedback and any issues found
