---
description: Standard task execution (4 agents)
argument-hint: <task-description>
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task, TodoWrite
---

# imlazy Standard Workflow

Execute a 4-agent workflow for standard development tasks.

## Task
$ARGUMENTS

---

## Workflow: 4 Agents

### Agent 1: Requirements Analyst

```
Read: ${CLAUDE_PLUGIN_ROOT}/agents/requirements-analyst.md
Read: ${CLAUDE_PLUGIN_ROOT}/skills/requirements-analysis/SKILL.md
```

Use Task tool with `subagent_type: general-purpose`:
- Include agent system prompt + skill knowledge
- Task: $ARGUMENTS
- Analyze requirements and clarify scope

---

### Agent 2: Code Analyst

```
Read: ${CLAUDE_PLUGIN_ROOT}/agents/code-analyst.md
Read: ${CLAUDE_PLUGIN_ROOT}/skills/code-analysis/SKILL.md
```

Use Task tool with `subagent_type: general-purpose`:
- Include agent system prompt + skill knowledge
- Include Requirements Analyst's output
- Analyze existing codebase for relevant patterns and impact areas

---

### Agent 3: Developer

```
Read: ${CLAUDE_PLUGIN_ROOT}/agents/developer.md
Read: ${CLAUDE_PLUGIN_ROOT}/skills/implementation/SKILL.md
```

Use Task tool with `subagent_type: general-purpose`:
- Include agent system prompt + skill knowledge
- Include previous agents' outputs (requirements + code analysis)
- Implement the solution

---

### Agent 4: Reviewer

```
Read: ${CLAUDE_PLUGIN_ROOT}/agents/reviewer.md
Read: ${CLAUDE_PLUGIN_ROOT}/skills/code-review/SKILL.md
```

Use Task tool with `subagent_type: general-purpose`:
- Include agent system prompt + skill knowledge
- Include all previous outputs
- Review the implementation for quality and correctness

---

## Completion

After all 4 agents complete, provide a summary:
- Requirements analysis findings
- Code analysis insights
- Implementation summary
- Review results and any issues found
