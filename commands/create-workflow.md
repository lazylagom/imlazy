---
description: Interactively create a new custom workflow
argument-hint: [workflow-name]
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion, TodoWrite
---

# imlazy Create Workflow

Create a new custom workflow with associated agents, skills, and commands.

## Workflow Creation Process

### Step 1: Get Workflow Name

If $ARGUMENTS is provided, use it as the workflow name.
Otherwise, use AskUserQuestion to ask:
- "What is the name of your new workflow?" (e.g., "design", "refactor", "debug")

The workflow name will be used with `lazy-` prefix for all components.

### Step 2: Gather Workflow Details

Use AskUserQuestion to ask:

1. "What is this workflow for?" (description)
2. "How many agents should this workflow have?" (1-5)
3. For each agent:
   - "What is the role of agent {n}?" (e.g., "analyzer", "implementer", "validator")
   - "What skills should this agent use?" (can be existing or new)

### Step 3: Create Components

Based on the answers, create the following with `lazy-{name}-` prefix:

#### 3.1 Create Command
Create `commands/lazy-{name}.md`:
```markdown
---
description: Execute {name} workflow
argument-hint: <task-description>
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task, TodoWrite
---

# imlazy {Name} Workflow

Execute the {name} workflow.

## Task
$ARGUMENTS

## Execution Steps
{Generate steps based on agents defined}
```

#### 3.2 Create Agents
For each agent, create `agents/lazy-{name}-{role}.md`:
```markdown
---
name: lazy-{name}-{role}
model: sonnet
tools: [Read, Write, Edit, Bash, Glob, Grep]
---

# Lazy {Name} {Role} Agent

{Role description and instructions}
```

#### 3.3 Create Skills (if new skills needed)
For each new skill, create `skills/lazy-{name}-{skill}/SKILL.md`:
```markdown
---
name: lazy-{name}-{skill}
description: {Skill description}
---

# {Skill Name}

{Skill content}
```

### Step 4: Update .workflow.yaml

Read the current `.workflow.yaml` and add the new workflow:

```yaml
lazy-{name}:
  description: "{workflow description}"
  agents:
    - name: lazy-{name}-{role1}
      skills:
        - {skill1}
    - name: lazy-{name}-{role2}
      skills:
        - {skill2}
```

### Step 5: Summary

After creation, display:
- Created command: `/imlazy:lazy-{name}`
- Created agents: list of agent files
- Created skills: list of skill directories (if any)
- Updated: `.workflow.yaml`

Explain how to use the new workflow:
```
/imlazy:lazy-{name} <your task description>
```

## Example

If user inputs "design":

Created files:
- `commands/lazy-design.md`
- `agents/lazy-design-analyst.md`
- `agents/lazy-design-designer.md`
- `skills/lazy-design-patterns/SKILL.md`
- Updated `.workflow.yaml` with `lazy-design` workflow

Usage: `/imlazy:lazy-design Create a new user authentication system`
