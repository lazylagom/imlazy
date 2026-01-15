# imlazy

> **Stay Lazy, Act Crazy**

Simple agent workflow plugin for Claude Code. Run predefined SDLC-based agent workflows for development tasks.

## Overview

imlazy provides structured multi-agent workflows for software development. Choose a complexity level and let the agents handle the rest.

## Installation

Copy the plugin to your project or test directly:

```bash
claude --plugin-dir /path/to/imlazy
```

## Commands

| Command | Description | Agents |
|---------|-------------|--------|
| `/imlazy:on` | Activate with greeting | - |
| `/imlazy:low` | Quick workflow | 2 agents |
| `/imlazy:medium` | Standard workflow | 4 agents |
| `/imlazy:high` | Full SDLC | 5 agents |

## Workflows

### Low (2 agents)
**requirements-analyst** → **developer**

Best for: Simple tasks, quick fixes, small features

### Medium (4 agents)
**requirements-analyst** → **code-analyst** → **developer** → **reviewer**

Best for: Standard features, bug fixes with investigation

### High (5 agents)
**requirements-analyst** → **code-analyst** → **architect** → **developer** → **reviewer**

Best for: Complex features, architectural changes, major refactoring

## Agents

| Agent | Role | Model |
|-------|------|-------|
| requirements-analyst | Analyze and clarify requirements | Sonnet |
| code-analyst | Explore and analyze existing codebase | Sonnet |
| architect | Design solution architecture | Opus |
| developer | Implement code and tests | Sonnet |
| reviewer | Review code quality and correctness | Sonnet |

## Skills

Each agent has access to domain-specific knowledge:

| Skill | Description |
|-------|-------------|
| requirements-analysis | Requirements gathering, MoSCoW prioritization |
| code-analysis | Codebase exploration, pattern recognition |
| system-design | Architecture patterns, component design |
| implementation | Code structure, coding best practices |
| testing | Test strategies, TDD practices |
| code-review | Quality review, security assessment |

## Project Structure

```
imlazy/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   ├── on.md
│   ├── low.md
│   ├── medium.md
│   └── high.md
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
└── hooks/
    ├── hooks.json
    └── scripts/
        └── init-session.sh
```

## Usage

```
# Quick task
/imlazy:low Fix the typo in login validation

# Standard development
/imlazy:medium Add user profile page

# Complex feature
/imlazy:high Implement user authentication system
```

## How It Works

1. You invoke a workflow command with a task description
2. Each agent in the sequence executes in order
3. Agents read their role definition and skill knowledge
4. Each agent receives context from previous agents
5. Final summary provided after all agents complete

## License

MIT
