# imlazy

> **Stay Lazy, Think Crazy**

A cognitive agent workflow system for Claude Code. Cyclic architecture with reflexion and memory.

## Core Philosophy

Instead of linear workflows, this implements **how agents should think**:

- **Cyclic Graph**: Failure → Reflect → Retry (not linear waterfall)
- **Test Anchoring**: Verified tests become immutable anchors
- **4-Tier Memory**: Learn from past episodes
- **Reflexion**: Self-correct through 5 Whys analysis

## Installation

### Marketplace (Recommended)

```
/plugin marketplace add lazylagom/lazy-marketplace
/plugin install imlazy
```

### Manual

```bash
git clone https://github.com/lazylagom/imlazy.git ~/.claude/plugins/imlazy
```

### Verify

```
/imlazy:doctor
```

## Commands

| Command | Description |
|---------|-------------|
| `/imlazy:think <task>` | Main cognitive workflow |
| `/imlazy:memory <action>` | Memory search/store/stats |
| `/imlazy:state [action]` | View/manage cognitive state |
| `/imlazy:doctor` | Plugin health check |

## Architecture

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

### Nodes

| Node | Model | Purpose |
|------|-------|---------|
| **PLANNER** | sonnet | Memory retrieval + AlphaCodium problem analysis |
| **REASONER** | opus | Tree of Thoughts deep reasoning |
| **CODER** | sonnet | Implementation with test anchoring |
| **VERIFIER** | haiku | Test execution and validation |
| **REFLECTOR** | opus | Reflexion self-correction (5 Whys) |
| **CONSOLIDATOR** | haiku | Archive episode to long-term memory |

### Key Mechanisms

**AlphaCodium Preprocessing** (PLANNER)
- Structured problem reflection
- Generate 2-3 solutions with tradeoffs
- Select best approach

**Tree of Thoughts** (REASONER)
- Explore multiple reasoning paths
- Score on correctness, simplicity, robustness

**Test Anchoring** (CODER)
- Passed tests become immutable anchors
- Anchor failure → immediate revert
- Monotonic progress guaranteed

**Reflexion** (REFLECTOR)
- 5 Whys root cause analysis
- Self-critique and corrections
- Smart routing back to appropriate node

## Memory System

4-tier cognitive memory at `~/.imlazy/`:

| Type | Purpose |
|------|---------|
| **Working** | Current episode state |
| **Episodic** | Past problem-solution pairs |
| **Semantic** | Domain knowledge, patterns |
| **Procedural** | Learned strategies, corrections |

```bash
# Search past experiences
/imlazy:memory search episodic "authentication"

# View memory stats
/imlazy:memory stats
```

## Cognitive State

Track the thinking process:

```bash
# View full state
/imlazy:state

# Get specific field
/imlazy:state get current_node
/imlazy:state get retry_count
```

## Usage Examples

```bash
# Full cognitive workflow
/imlazy:think add user authentication

# Check current state
/imlazy:state

# Search memory
/imlazy:memory search episodic "login"
```

## Flow Examples

### Simple Bug Fix
```
PLANNER → CODER → VERIFIER → CONSOLIDATOR
(REASONER skipped - cause is obvious)
```

### Complex Feature with Failure
```
PLANNER → REASONER → CODER → VERIFIER(fail)
  → REFLECTOR → CODER(fix) → VERIFIER(pass)
  → CONSOLIDATOR
```

### Deep Problem Requiring Reanalysis
```
PLANNER → REASONER → CODER → VERIFIER(fail)
  → REFLECTOR → PLANNER(reanalyze)
  → REASONER → CODER → VERIFIER(pass)
  → CONSOLIDATOR
```

## Project Structure

```
imlazy/
├── .claude-plugin/plugin.json
├── agents/
│   ├── planner.md
│   ├── reasoner.md
│   ├── coder.md
│   ├── verifier.md
│   ├── reflector.md
│   └── consolidator.md
├── commands/
│   ├── think.md
│   ├── memory.md
│   ├── state.md
│   └── doctor.md
├── skills/
│   ├── cognitive-state/
│   ├── memory-system/
│   └── alphacodium-flow/
└── hooks/
    ├── hooks.json
    └── scripts/
        ├── state-manager.py
        ├── memory-manager.py
        ├── reflection-trigger.py
        ├── bash-validator.py
        ├── file-protector.py
        ├── init-session.sh
        └── auto-formatter.sh
```

## Hooks

Automated safety and quality:

| Hook | Trigger | Purpose |
|------|---------|---------|
| **bash-validator** | PreToolUse | Block dangerous commands |
| **file-protector** | PreToolUse | Protect .env, *.lock |
| **auto-formatter** | PostToolUse | Run prettier/black |
| **reflection-trigger** | PostToolUse | Auto-detect test failures |

## vs Traditional Approaches

| Traditional | imlazy |
|-------------|--------|
| Linear 5-step workflow | Cyclic graph with reflexion |
| Manual error handling | Automatic REFLECTOR routing |
| No memory | 4-tier memory system |
| Single attempt | Up to 3 retries with learning |
| Template filling | Structured cognitive process |

## License

MIT
