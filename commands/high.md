---
description: Full SDLC workflow (5 agents)
argument-hint: <task-description>
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task, TodoWrite
---

# imlazy Full SDLC Workflow

Execute the complete 5-agent SDLC workflow for complex tasks.

## Task
$ARGUMENTS

---

## Workflow: 5 Agents

### Agent 1: Requirements Analyst

```
Read: ${CLAUDE_PLUGIN_ROOT}/agents/requirements-analyst.md
Read: ${CLAUDE_PLUGIN_ROOT}/skills/requirements-analysis/SKILL.md
```

Use Task tool with `subagent_type: general-purpose`:
- Include agent system prompt + skill knowledge
- Task: $ARGUMENTS
- Analyze requirements, clarify scope, identify acceptance criteria

---

### Agent 2: Code Analyst

```
Read: ${CLAUDE_PLUGIN_ROOT}/agents/code-analyst.md
Read: ${CLAUDE_PLUGIN_ROOT}/skills/code-analysis/SKILL.md
```

Use Task tool with `subagent_type: general-purpose`:
- Include agent system prompt + skill knowledge
- Include Requirements Analyst's output
- Analyze existing codebase, identify patterns, assess impact

---

### Agent 3: Architect

```
Read: ${CLAUDE_PLUGIN_ROOT}/agents/architect.md
Read: ${CLAUDE_PLUGIN_ROOT}/skills/system-design/SKILL.md
```

Use Task tool with `subagent_type: general-purpose`:
- Include agent system prompt + skill knowledge
- Include previous agents' outputs (requirements + code analysis)
- Design the solution architecture and make technical decisions

---

### Agent 4: Developer

```
Read: ${CLAUDE_PLUGIN_ROOT}/agents/developer.md
Read: ${CLAUDE_PLUGIN_ROOT}/skills/implementation/SKILL.md
Read: ${CLAUDE_PLUGIN_ROOT}/skills/testing/SKILL.md
```

Use Task tool with `subagent_type: general-purpose`:
- Include agent system prompt + skill knowledge (implementation + testing)
- Include all previous outputs (requirements, analysis, architecture)
- Implement the solution with tests

---

### Agent 5: Reviewer

```
Read: ${CLAUDE_PLUGIN_ROOT}/agents/reviewer.md
Read: ${CLAUDE_PLUGIN_ROOT}/skills/code-review/SKILL.md
```

Use Task tool with `subagent_type: general-purpose`:
- Include agent system prompt + skill knowledge
- Include all previous outputs
- Review implementation quality, security, and requirements compliance

---

## Completion

After all 5 agents complete, provide a comprehensive summary:
- Requirements and scope
- Codebase analysis findings
- Architecture decisions
- Implementation details
- Review findings and recommendations
