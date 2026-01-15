---
description: Execute high complexity workflow (full SDLC)
argument-hint: <task-description>
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task, TodoWrite
---

# imlazy High Complexity Workflow

Execute a high complexity workflow for complex development tasks requiring full SDLC coverage.

## Task
$ARGUMENTS

## Workflow Execution

1. Read the workflow configuration from `${CLAUDE_PLUGIN_ROOT}/.workflow.yaml`
2. Find the `high` workflow definition
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

### Step 3: Architect
Use the Task tool to launch the `architect` agent with:
- Requirements and code analysis from previous steps
- Skills to use: system-design
- Save output to `.imlazy/context/{session}/03-architect.md`

### Step 4: Developer
Use the Task tool to launch the `developer` agent with:
- All previous context including architecture design
- Skills to use: implementation, testing
- Save output to `.imlazy/context/{session}/04-developer.md`

### Step 5: Reviewer
Use the Task tool to launch the `reviewer` agent with:
- All previous context
- Skills to use: code-review
- Save output to `.imlazy/context/{session}/05-reviewer.md`

## Context Management
- Create session directory: `.imlazy/context/{timestamp}/`
- Each agent saves their output to the context directory
- Pass previous agent's output to the next agent

## Completion
After all agents complete, provide a comprehensive summary of:
- Requirements analyzed and clarified
- Existing code analysis and impact assessment
- Architecture decisions and design rationale
- Implementation details and test coverage
- Review feedback, quality assessment, and recommendations
