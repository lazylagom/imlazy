---
name: cognitive-state
description: Manage and inspect the CognitiveState working memory for cognitive episodes. Use when viewing current workflow state, checking node transitions, inspecting problem reflections, accessing thought traces, managing anchor tests, debugging workflow issues, or understanding the state schema and lifecycle.
allowed-tools: Bash, Read
---

# Cognitive State Management

The CognitiveState is the working memory of the imlazy workflow system. It maintains all context needed for the current cognitive episode.

## Schema

```yaml
CognitiveState:
  # Task Definition
  user_query: string # Original user request
  problem_reflection: # AlphaCodium-style preprocessing
    goal: string # Single sentence objective
    inputs: list # Required inputs
    outputs: list # Expected outputs
    constraints: list # Constraints and requirements
    edge_cases: list # Edge cases to handle

  # Thought Process
  current_plan: list # Current execution plan
  thought_trace: list # Chain-of-thought log
  critiques: list # Self-critiques from Reflexion
  possible_solutions: list # Candidate solutions
  selected_solution: string # Chosen solution

  # Execution Context
  file_context: dict # Relevant files and snippets
  test_results:
    public_tests: list # User-provided tests
    ai_tests: list # AI-generated edge case tests
    anchor_tests: list # Verified tests (immutable)
  error_log: list # Errors encountered

  # Cycle Control
  current_node: string # Current workflow node
  retry_count: int # Current retry count
  max_retries: 3 # Maximum retries before escalation

  # Metadata
  episode_id: string # Unique episode identifier
  project_hash: string # Project identifier
  created_at: string # ISO timestamp
  updated_at: string # ISO timestamp
```

## Node Transitions

Valid nodes: `PLANNER`, `REASONER`, `CODER`, `VERIFIER`, `REFLECTOR`, `CONSOLIDATOR`

```
PLANNER → REASONER → CODER → VERIFIER → CONSOLIDATOR
    ↑         ↑         ↑         ↓
    └─────────┴─────────┴─────────┘
           (via REFLECTOR)
```

## State Operations

### Initialize New Episode

```bash
python3 hooks/scripts/state-manager.py init
```

### Get State

```bash
# Get entire state
python3 hooks/scripts/state-manager.py dump

# Get specific field
python3 hooks/scripts/state-manager.py get current_node
python3 hooks/scripts/state-manager.py get problem_reflection.goal
```

### Update State

```bash
# Set simple value
python3 hooks/scripts/state-manager.py set user_query "Add login feature"

# Set nested value
python3 hooks/scripts/state-manager.py set problem_reflection.goal "Implement user authentication"

# Append to list
python3 hooks/scripts/state-manager.py update thought_trace '{"type":"thought","content":"Analyzing requirements"}'
```

### Node Transitions

```bash
python3 hooks/scripts/state-manager.py transition REASONER
```

## State Lifecycle

1. **Init**: New episode starts, state initialized
2. **PLANNER**: Populates `problem_reflection`, `possible_solutions`, `selected_solution`
3. **REASONER**: Updates `thought_trace`, refines `current_plan`
4. **CODER**: Updates `file_context`, `test_results.ai_tests`
5. **VERIFIER**: Updates `test_results`, may add to `error_log`
6. **REFLECTOR**: Adds to `critiques`, increments `retry_count`
7. **CONSOLIDATOR**: Final state archived to episodic memory

## Anchor Tests

Anchor tests are immutable once verified:

- Start empty
- When a test passes, it becomes an anchor
- If any anchor test fails after a code change, the change must be reverted
- This ensures monotonic progress

```python
# Pseudo-logic
for change in code_changes:
    apply(change)
    if any(anchor_test.fails() for anchor_test in anchor_tests):
        revert(change)
        route_to_reflector("Anchor test regression")
    else:
        new_passing = [t for t in new_tests if t.passes()]
        anchor_tests.extend(new_passing)
```

## Error Handling

- `retry_count` increments on each REFLECTOR visit
- When `retry_count >= max_retries`, escalate to user
- `error_log` preserves all errors for analysis

## Storage

- Location: `~/.imlazy/working/state.json`
- Persists across agent invocations
- Cleared on `init` or `reset`
