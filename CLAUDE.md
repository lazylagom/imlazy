# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

imlazy (Cognitive Agent Loop Architecture) is a Claude Code plugin implementing a cyclic cognitive agent workflow inspired by the imlazy paper. It combines AlphaCodium-style problem preprocessing, Tree of Thoughts reasoning, test anchoring, and Reflexion-based self-correction.

**Core philosophy:** Give agents time to think and mirrors to reflect - deep thought loops over complex multi-agent systems.

## Plugin Structure

```
imlazy/
├── .claude-plugin/plugin.json    # Plugin manifest
├── CLAUDE.md                     # This file
│
├── agents/                       # 6 cognitive nodes
│   ├── planner.md               # Memory retrieval + AlphaCodium preprocessing
│   ├── reasoner.md              # Tree of Thoughts deep reasoning
│   ├── coder.md                 # Implementation + test anchoring
│   ├── verifier.md              # Test execution
│   ├── reflector.md             # Reflexion self-correction
│   └── consolidator.md          # Memory consolidation
│
├── commands/                     # Slash commands
│   ├── think.md                 # Main orchestration
│   ├── memory.md                # Memory management
│   ├── state.md                 # State inspection
│   └── doctor.md                # Health check
│
├── skills/                       # Documentation
│   ├── cognitive-state/SKILL.md # State schema docs
│   ├── memory-system/SKILL.md   # 4-tier memory docs
│   └── alphacodium-flow/SKILL.md # AlphaCodium docs
│
└── hooks/                        # Automation
    ├── hooks.json               # Hook configuration
    └── scripts/
        ├── state-manager.py     # CognitiveState CRUD
        ├── memory-manager.py    # 4-tier memory CRUD
        ├── reflection-trigger.py # Auto-reflexion on failure
        ├── bash-validator.py    # Command safety
        ├── file-protector.py    # File protection
        ├── init-session.sh      # Session init
        └── auto-formatter.sh    # Code formatting
```

Runtime memory (`~/.imlazy/`):
```
~/.imlazy/
├── working/state.json    # Working Memory (current episode)
├── episodic/             # Past problem-solution pairs
├── semantic/             # Domain knowledge, patterns
└── procedural/           # Learned methods, corrections
```

## Development Commands

**Testing the plugin locally:**
```bash
claude --plugin-dir /path/to/imlazy
```

**Verify plugin health:**
```
/imlazy:doctor
```

**Memory operations:**
```
/imlazy:memory search episodic "query"
/imlazy:memory stats
```

**State inspection:**
```
/imlazy:state
/imlazy:state get current_node
```

## Architecture: Six-Node Cognitive Workflow

```
                    ┌──────────────────────────────────────────┐
                    │                                          │
                    ▼                                          │
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│ PLANNER │───▶│ REASONER│───▶│  CODER  │───▶│VERIFIER │───▶│REFLECTOR│
└─────────┘    └─────────┘    └─────────┘    └─────────┘    └─────────┘
   (sonnet)      (opus)        (sonnet)       (haiku)        (opus)
                                                  │
                                                  ▼
                                            ┌───────────┐
                                            │CONSOLIDATOR│
                                            └───────────┘
                                               (haiku)
```

| Node | Purpose | Key Technique |
|------|---------|---------------|
| PLANNER | Memory search + problem analysis | AlphaCodium preprocessing |
| REASONER | Deep deliberation | Tree of Thoughts |
| CODER | Implementation | Test Anchoring |
| VERIFIER | Validation | Test execution |
| REFLECTOR | Self-correction | Reflexion (5 Whys) |
| CONSOLIDATOR | Memory archival | Experience consolidation |

## CognitiveState Schema

```yaml
CognitiveState:
  user_query: string
  problem_reflection:
    goal: string
    inputs: list
    outputs: list
    constraints: list
    edge_cases: list
  current_plan: list
  thought_trace: list
  critiques: list
  possible_solutions: list
  selected_solution: string
  file_context: dict
  test_results:
    public_tests: list
    ai_tests: list
    anchor_tests: list    # Immutable once verified
  error_log: list
  current_node: string    # PLANNER|REASONER|CODER|VERIFIER|REFLECTOR|CONSOLIDATOR
  retry_count: int
  max_retries: 3
  episode_id: string
  project_hash: string
```

## Key Mechanisms

### 1. AlphaCodium Preprocessing (PLANNER)
- Structured problem reflection (goal, inputs, outputs, constraints, edge cases)
- Generate 2-3 possible solutions with tradeoffs
- Select best solution with reasoning
- Generate AI tests for edge cases

### 2. Tree of Thoughts (REASONER)
- Explore multiple reasoning paths for key decisions
- Score paths on correctness, simplicity, robustness
- Select and justify best path
- Generate detailed implementation plan

### 3. Test Anchoring (CODER)
- Anchor tests are immutable once verified
- If any anchor test fails after a change, REVERT immediately
- New passing tests become anchors
- Ensures monotonic progress (no regressions)

### 4. Reflexion (REFLECTOR)
- 5 Whys root cause analysis
- Self-critique of faulty assumptions
- Generate specific corrections for PLANNER/REASONER/CODER
- Route to appropriate node or escalate to user

## Agent File Format

Each agent is Markdown with YAML frontmatter:

```yaml
---
name: agent-name
description: |
  Multi-line description
model: sonnet|haiku|opus
color: terminal-color
tools: ["Read", "Grep", "Glob", ...]
---
```

## Routing Rules

| Condition | Route To |
|-----------|----------|
| VERIFIER passes | CONSOLIDATOR |
| VERIFIER fails | REFLECTOR |
| Anchor test violation | REFLECTOR (immediate) |
| REFLECTOR: simple bug | CODER |
| REFLECTOR: plan flaw | REASONER |
| REFLECTOR: problem misunderstood | PLANNER |
| retry_count >= 3 | User escalation |

## Memory System

| Type | Content | Example |
|------|---------|---------|
| Working | Current episode state | state.json |
| Episodic | Past problem-solution pairs | "Fixed login with JWT" |
| Semantic | Domain knowledge | "Uses Repository pattern" |
| Procedural | Learned strategies | "Always check null first" |

## Hooks System

| Hook | Trigger | Script |
|------|---------|--------|
| SessionStart | Plugin loads | init-session.sh |
| PreToolUse (Bash) | Before commands | bash-validator.py |
| PreToolUse (Edit/Write) | Before file edits | file-protector.py |
| PostToolUse (Edit/Write) | After file edits | auto-formatter.sh |
| PostToolUse (Bash) | After commands | reflection-trigger.py |

## Anti-Patterns to Avoid

- Linear waterfall workflows (use cyclic graph instead)
- Fixed phase sequences (allow skipping REASONER for simple tasks)
- Manual loopback decisions (use automatic Reflexion)
- Single memory store (use 4-tier memory system)
- Template-filling exercises (use hypothesis-driven thinking)
