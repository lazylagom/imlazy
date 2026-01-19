# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

## Project Overview

imlazy is a Claude Code plugin implementing an **Adaptive Cognitive Workflow System** - a cyclic agent architecture that combines AlphaCodium-style preprocessing, Tree of Thoughts reasoning, test anchoring, and Reflexion-based self-correction.

**Core philosophy:** Give agents time to think and mirrors to reflect.

## Plugin Structure

```
imlazy/
├── .claude-plugin/plugin.json
├── CLAUDE.md
├── README.md
│
├── agents/                       # 6 cognitive nodes
│   ├── planner.md               # Memory retrieval + problem analysis
│   ├── reasoner.md              # Tree of Thoughts reasoning
│   ├── coder.md                 # Implementation + test anchoring
│   ├── verifier.md              # Test execution
│   ├── reflector.md             # Reflexion self-correction
│   └── consolidator.md          # Memory consolidation
│
├── commands/
│   ├── think.md                 # Main orchestration (/imlazy:think)
│   ├── memory.md                # Memory management (/imlazy:memory)
│   ├── state.md                 # State inspection (/imlazy:state)
│   └── doctor.md                # Health check (/imlazy:doctor)
│
├── skills/
│   ├── cognitive-state/SKILL.md # CognitiveState schema docs
│   ├── memory-system/SKILL.md   # 4-tier memory system docs
│   └── alphacodium-flow/SKILL.md # AlphaCodium methodology docs
│
└── hooks/
    ├── hooks.json
    └── scripts/
        ├── state-manager.py     # CognitiveState CRUD
        ├── memory-manager.py    # 4-tier memory CRUD
        ├── reflection-trigger.py # Auto-reflexion on failure
        ├── bash-validator.py    # Block dangerous commands
        ├── file-protector.py    # Protect sensitive files
        ├── init-session.sh      # Session initialization
        └── auto-formatter.sh    # Code formatting
```

## Runtime Memory

Located at `~/.imlazy/`:
```
~/.imlazy/
├── working/state.json    # Current episode state
├── episodic/             # Past problem-solution pairs
├── semantic/             # Domain knowledge, patterns
└── procedural/           # Learned methods, corrections
```

## Architecture: 6-Node Cognitive Workflow

```
                    ┌──────────────────────────────────────────┐
                    │              (on failure)                │
                    ▼                                          │
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│ PLANNER │───▶│ REASONER│───▶│  CODER  │───▶│VERIFIER │───▶│REFLECTOR│
└─────────┘    └─────────┘    └─────────┘    └─────────┘    └─────────┘
   (sonnet)      (opus)        (sonnet)       (haiku)        (opus)
                                                  │
                                                  ▼ (on success)
                                            ┌───────────┐
                                            │CONSOLIDATOR│
                                            └───────────┘
                                               (haiku)
```

| Node | Model | Purpose | Key Technique |
|------|-------|---------|---------------|
| PLANNER | sonnet | Memory search + problem analysis | AlphaCodium preprocessing |
| REASONER | opus | Deep deliberation | Tree of Thoughts |
| CODER | sonnet | Implementation | Test Anchoring |
| VERIFIER | haiku | Validation | Test execution |
| REFLECTOR | opus | Self-correction | Reflexion (5 Whys) |
| CONSOLIDATOR | haiku | Memory archival | Experience consolidation |

## Commands

| Command | Description |
|---------|-------------|
| `/imlazy:think <task>` | Main cognitive workflow |
| `/imlazy:memory <action>` | Memory search/store/stats/prune |
| `/imlazy:state [action]` | View/manage cognitive state |
| `/imlazy:doctor` | Plugin health check |

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
  current_node: string
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

### 2. Tree of Thoughts (REASONER)
- Explore multiple reasoning paths
- Score paths on correctness, simplicity, robustness
- Generate detailed implementation plan

### 3. Test Anchoring (CODER)
- Anchor tests are immutable once verified
- If any anchor test fails → REVERT immediately
- Ensures monotonic progress (no regressions)

### 4. Reflexion (REFLECTOR)
- 5 Whys root cause analysis
- Self-critique of faulty assumptions
- Route to appropriate node or escalate

## Routing Rules

| Condition | Route To |
|-----------|----------|
| VERIFIER passes | CONSOLIDATOR |
| VERIFIER fails | REFLECTOR |
| Anchor violation | REFLECTOR (immediate revert) |
| REFLECTOR: simple bug | CODER |
| REFLECTOR: plan flaw | REASONER |
| REFLECTOR: problem misunderstood | PLANNER |
| retry_count >= 3 | User escalation |

## 4-Tier Memory System

| Type | Purpose | Location |
|------|---------|----------|
| Working | Current episode state | `~/.imlazy/working/` |
| Episodic | Past problem-solution pairs | `~/.imlazy/episodic/` |
| Semantic | Domain knowledge, patterns | `~/.imlazy/semantic/` |
| Procedural | Learned strategies | `~/.imlazy/procedural/` |

## Hooks

| Event | Script | Purpose |
|-------|--------|---------|
| SessionStart | init-session.sh | Initialize session |
| PreToolUse (Bash) | bash-validator.py | Block dangerous commands |
| PreToolUse (Edit/Write) | file-protector.py | Protect .env, *.lock |
| PostToolUse (Edit/Write) | auto-formatter.sh | Run prettier/black |
| PostToolUse (Bash) | reflection-trigger.py | Auto-detect test failures |

## Development

**Test plugin locally:**
```bash
claude --plugin-dir /path/to/imlazy
```

**Verify health:**
```
/imlazy:doctor
```

**Memory operations:**
```
/imlazy:memory stats
/imlazy:memory search episodic "query"
```

**State inspection:**
```
/imlazy:state
/imlazy:state get current_node
```
