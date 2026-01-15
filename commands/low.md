---
description: Quick task execution (2 agents)
argument-hint: <task-description>
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task, TodoWrite
---

# imlazy Quick Workflow

Execute a quick 2-agent workflow for simple tasks.

## Task
$ARGUMENTS

---

## Workflow: 2 Agents

### Agent 1: Requirements Analyst

First, read the agent definition and skill, then execute:

```
Read: ${CLAUDE_PLUGIN_ROOT}/agents/requirements-analyst.md
Read: ${CLAUDE_PLUGIN_ROOT}/skills/requirements-analysis/SKILL.md
```

Use Task tool with `subagent_type: general-purpose`:
- Include the agent system prompt
- Include the skill knowledge
- Task: $ARGUMENTS
- Ask the agent to analyze requirements and clarify scope

Save the output mentally - you'll pass it to the next agent.

---

### Agent 2: Developer

Read the agent definition and skill:

```
Read: ${CLAUDE_PLUGIN_ROOT}/agents/developer.md
Read: ${CLAUDE_PLUGIN_ROOT}/skills/implementation/SKILL.md
```

Use Task tool with `subagent_type: general-purpose`:
- Include the agent system prompt
- Include the skill knowledge
- Include the Requirements Analyst's output as context
- Task: $ARGUMENTS
- Ask the agent to implement the solution

---

## Completion

After both agents complete, provide a summary:
- What the Requirements Analyst found
- What the Developer implemented
- Any follow-up actions needed
