# imlazy

> **Stay Lazy, Act Crazy**

Adaptive Agent Workflow plugin for Claude Code. Create and run your own customizable agent workflows tailored to your development process.

## Overview

imlazy provides a flexible framework for orchestrating multiple AI agents in a structured workflow. Each workflow defines a sequence of specialized agents, with each agent having access to specific skills for their role.

**Key Features:**
- Pre-defined workflows for different complexity levels (low, medium, high)
- SDLC-based agents (requirements analyst, code analyst, architect, developer, reviewer)
- Customizable workflow definitions via YAML
- Context preservation between agent executions
- Easy creation of custom workflows

## Installation

imlazy is designed for project-local installation. Copy the plugin to your project:

```bash
# Clone or copy to your project
cp -r imlazy/.claude-plugin your-project/.claude-plugin
cp -r imlazy/commands your-project/commands
cp -r imlazy/agents your-project/agents
cp -r imlazy/skills your-project/skills
cp -r imlazy/hooks your-project/hooks
cp -r imlazy/scripts your-project/scripts
cp imlazy/.workflow.yaml your-project/.workflow.yaml
```

Or test directly:

```bash
claude --plugin-dir /path/to/imlazy
```

## Commands

| Command | Description |
|---------|-------------|
| `/imlazy:on` | Activate imlazy with greeting message |
| `/imlazy:low` | Execute low complexity workflow (quick tasks) |
| `/imlazy:medium` | Execute medium complexity workflow (standard tasks) |
| `/imlazy:high` | Execute high complexity workflow (full SDLC) |
| `/imlazy:create-workflow` | Interactively create a new custom workflow |

## Workflows

### Low Complexity
For simple, straightforward tasks. Agents: requirements-analyst → developer

### Medium Complexity
For standard development tasks. Agents: requirements-analyst → code-analyst → developer → reviewer

### High Complexity
For complex tasks requiring full SDLC coverage. Agents: requirements-analyst → code-analyst → architect → developer → reviewer

## Agents

| Agent | Role | Color |
|-------|------|-------|
| requirements-analyst | Analyze and clarify requirements | Cyan |
| code-analyst | Explore and analyze existing codebase | Blue |
| architect | Design solution architecture | Green |
| developer | Implement code and tests | Magenta |
| reviewer | Review code quality and correctness | Yellow |

## Skills

| Skill | Purpose |
|-------|---------|
| requirements-analysis | Requirements gathering and documentation |
| code-analysis | Codebase exploration and pattern recognition |
| system-design | Architecture and design patterns |
| implementation | Coding best practices |
| testing | Test strategies and TDD |
| code-review | Code review checklists and practices |

## Workflow Configuration

Workflows are defined in `.workflow.yaml`:

```yaml
workflows:
  my-custom-workflow:
    description: "My custom workflow"
    agents:
      - name: requirements-analyst
        skills:
          - requirements-analysis
      - name: developer
        skills:
          - implementation
          - testing
```

## Creating Custom Workflows

Use `/imlazy:create-workflow` to interactively create new workflows:

1. Provide a workflow name (e.g., "design")
2. Define agents and their skills
3. The command creates:
   - `commands/lazy-{name}.md`
   - `agents/lazy-{name}-*.md`
   - `skills/lazy-{name}-*/SKILL.md`
   - Updates `.workflow.yaml`

## Context Management

Each workflow execution creates a session in `.imlazy/context/`:

```
.imlazy/
└── context/
    └── 20250115_103045/
        ├── 01-requirements-analyst.md
        ├── 02-code-analyst.md
        ├── 03-architect.md
        ├── 04-developer.md
        └── 05-reviewer.md
```

Each agent's output is preserved and passed to subsequent agents.

## Project Structure

```
your-project/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   ├── on.md
│   ├── low.md
│   ├── medium.md
│   ├── high.md
│   └── create-workflow.md
├── agents/
│   ├── requirements-analyst.md
│   ├── code-analyst.md
│   ├── architect.md
│   ├── developer.md
│   └── reviewer.md
├── skills/
│   ├── requirements-analysis/
│   ├── code-analysis/
│   ├── system-design/
│   ├── implementation/
│   ├── testing/
│   └── code-review/
├── hooks/
│   ├── hooks.json
│   └── scripts/
├── scripts/
│   └── parse-workflow.sh
├── .workflow.yaml
└── .imlazy/          # Runtime data (gitignored)
    └── context/
```

## Utility Scripts

### parse-workflow.sh

Parse and query workflow configuration:

```bash
# List all workflows
./scripts/parse-workflow.sh list

# Get workflow details
./scripts/parse-workflow.sh get high

# List agents in a workflow
./scripts/parse-workflow.sh agents medium

# List skills used in a workflow
./scripts/parse-workflow.sh skills low
```

## Customization

### Adding Custom Agents

Create new agent files in `agents/`:

```markdown
---
name: my-custom-agent
description: |
  Use this agent when...
model: inherit
color: cyan
tools: ["Read", "Write", "Edit"]
---

Agent instructions here...
```

### Adding Custom Skills

Create new skill directories in `skills/`:

```
skills/my-skill/
└── SKILL.md
```

### Modifying Workflows

Edit `.workflow.yaml` to customize agent sequences and skill assignments.

## Best Practices

1. **Start with lower complexity**: Use `/imlazy:low` for simple tasks
2. **Review context**: Check `.imlazy/context/` to see agent outputs
3. **Customize per project**: Each project can have different workflow configurations
4. **Create domain-specific workflows**: Use `/imlazy:create-workflow` for specialized workflows

## Troubleshooting

**Commands not appearing:**
- Restart Claude Code after installing the plugin
- Check that files are in correct directories

**Workflow not executing:**
- Verify `.workflow.yaml` exists and is valid YAML
- Check that referenced agents exist in `agents/`

**Context not saving:**
- Ensure `.imlazy/` directory exists
- Check file permissions

## License

MIT
