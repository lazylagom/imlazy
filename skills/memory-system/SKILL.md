---
name: memory-system
description: Manage the 4-tier cognitive memory system (working, episodic, semantic, procedural). Use when searching past experiences, storing domain knowledge, recalling patterns, consolidating learnings, managing memory entries, pruning old memories, or understanding memory flow across workflow nodes.
allowed-tools: Bash, Read
---

# imlazy 4-Tier Memory System

The memory system implements a cognitive architecture inspired by human memory:

```
┌─────────────────────────────────────────────────────────────┐
│                     MEMORY SYSTEM                           │
├─────────────────────────────────────────────────────────────┤
│  Working Memory     │  Current episode state               │
│  (state.json)       │  Fast, volatile, single instance     │
├─────────────────────────────────────────────────────────────┤
│  Episodic Memory    │  Past problem-solution pairs         │
│  (~/.imlazy/episodic)│  "What I did before"                 │
├─────────────────────────────────────────────────────────────┤
│  Semantic Memory    │  Domain knowledge, patterns          │
│  (~/.imlazy/semantic)│  "What I know"                       │
├─────────────────────────────────────────────────────────────┤
│  Procedural Memory  │  Methods, strategies, corrections    │
│  (~/.imlazy/procedural)│  "How to do things"                │
└─────────────────────────────────────────────────────────────┘
```

## Memory Types

### Working Memory

- **Purpose**: Current cognitive state
- **Lifetime**: Single episode
- **Management**: `state-manager.py`
- **Location**: `~/.imlazy/working/state.json`

### Episodic Memory

- **Purpose**: Store past experiences
- **Content**: Problem-solution pairs, outcomes, thought traces
- **Use Case**: "I've solved something similar before"
- **Location**: `~/.imlazy/episodic/*.json`

### Semantic Memory

- **Purpose**: Domain knowledge and patterns
- **Content**: Code patterns, architecture decisions, API knowledge
- **Use Case**: "This codebase uses X pattern"
- **Location**: `~/.imlazy/semantic/*.json`

### Procedural Memory

- **Purpose**: Learned methods and corrections
- **Content**: Strategies, self-corrections from Reflexion
- **Use Case**: "Last time I made this mistake, I learned..."
- **Location**: `~/.imlazy/procedural/*.json`

## Operations

### Search Memory

```bash
# Search episodic memory for similar problems
python3 hooks/scripts/memory-manager.py search episodic "authentication login"

# Search semantic memory for patterns
python3 hooks/scripts/memory-manager.py search semantic "react hooks"

# Limit results
python3 hooks/scripts/memory-manager.py search procedural "error handling" --limit 3
```

### Store Memory

```bash
# Store semantic knowledge
python3 hooks/scripts/memory-manager.py store semantic '{"pattern":"singleton","context":"database connection"}' --tags pattern,database

# Store procedural learning
python3 hooks/scripts/memory-manager.py store procedural '{"learning":"Always check null before accessing","source":"bug fix"}' --tags null-check,learning
```

### Recall Specific Memory

```bash
python3 hooks/scripts/memory-manager.py recall abc123def456
```

### Consolidate Working to Episodic

```bash
# Called at end of successful episode
python3 hooks/scripts/memory-manager.py consolidate
```

### Statistics

```bash
python3 hooks/scripts/memory-manager.py stats
```

### Prune Old Memories

```bash
# Remove memories older than 30 days with zero access
python3 hooks/scripts/memory-manager.py prune --days 30
```

## Memory Entry Schema

```json
{
  "id": "abc123def456",
  "type": "episodic|semantic|procedural",
  "data": {
    // Type-specific content
  },
  "tags": ["tag1", "tag2"],
  "created_at": "2024-01-15T10:30:00",
  "access_count": 5,
  "last_accessed": "2024-01-20T14:00:00"
}
```

## Memory Flow in Workflow

```
┌──────────┐
│  PLANNER │ ← Search episodic: "Similar problems?"
│          │ ← Search semantic: "Relevant patterns?"
└────┬─────┘
     │
     ▼
┌──────────┐
│ REASONER │ ← Search procedural: "Known strategies?"
└────┬─────┘
     │
     ▼
┌──────────┐
│  CODER   │ ← Search semantic: "Code patterns?"
└────┬─────┘
     │
     ▼
┌──────────┐
│REFLECTOR │ → Store procedural: Corrections learned
└────┬─────┘
     │
     ▼
┌────────────┐
│CONSOLIDATOR│ → Store episodic: Complete experience
│            │ → Store semantic: New patterns discovered
└────────────┘
```

## Best Practices

1. **Search Before Acting**: PLANNER should always search episodic memory
2. **Tag Consistently**: Use consistent tags for better recall
3. **Consolidate Always**: Every successful episode should consolidate
4. **Store Corrections**: REFLECTOR learnings go to procedural memory
5. **Prune Regularly**: Remove old, unused memories to keep system fast

## Relevance Scoring

Current implementation uses keyword matching. Future improvements:

- Semantic embeddings for better similarity
- Recency weighting
- Access frequency boosting
- Project-specific filtering
