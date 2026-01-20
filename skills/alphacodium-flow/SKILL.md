---
name: alphacodium-flow
description: AlphaCodium code generation methodology with structured problem analysis, solution generation, and test anchoring. Use when implementing complex features, designing solutions, creating problem reflections, evaluating multiple approaches, generating AI tests, or implementing test-driven development with monotonic progress guarantees.
---

# AlphaCodium Flow

AlphaCodium is a code generation methodology that emphasizes structured problem analysis and iterative test-driven development.

## Core Principles

1. **Problem Reflection Before Coding**: Fully understand the problem before writing code
2. **Multiple Solutions**: Generate 2-3 distinct approaches, evaluate tradeoffs
3. **AI-Generated Tests**: Create edge case tests the user didn't provide
4. **Test Anchoring**: Once a test passes, it becomes immutable
5. **Iterative Refinement**: Fix issues against expanding test suite

## Problem Reflection Template

The PLANNER agent produces this structured analysis:

```markdown
## Problem Reflection

**Goal**: [Single sentence - the core objective]

**Inputs**:

- [Input 1]: [Type and description]
- [Input 2]: [Type and description]

**Outputs**:

- [Output 1]: [Type and description]
- [Expected format/structure]

**Constraints**:

- [Technical constraint]
- [Business rule]
- [Performance requirement]

**Edge Cases**:

- [Boundary condition 1]
- [Error scenario 1]
- [Unusual input 1]
```

## Solution Generation

Generate 2-3 distinct approaches:

```markdown
## Possible Solutions

### Solution A: [Descriptive Name]

**Approach**: [2-3 sentence description]
**Key Insight**: [Why this might work]
**Pros**:

- [Advantage 1]
- [Advantage 2]
  **Cons**:
- [Disadvantage 1]
- [Disadvantage 2]
  **Risk Level**: Low / Medium / High
  **Complexity**: O(n) / O(n log n) / O(n²)

### Solution B: [Descriptive Name]

...
```

## Solution Selection

Evaluate and choose:

```markdown
## Selection Matrix

| Criterion       | Solution A | Solution B | Solution C |
| --------------- | ---------- | ---------- | ---------- |
| Correctness     | 4/5        | 5/5        | 3/5        |
| Simplicity      | 5/5        | 3/5        | 4/5        |
| Performance     | 3/5        | 5/5        | 4/5        |
| Maintainability | 4/5        | 3/5        | 4/5        |
| **Total**       | 16/20      | 16/20      | 15/20      |

## Selected: Solution A

**Reasoning**: [Why this wins despite tied score, or clear winner reasoning]
```

## AI Test Generation

For each identified edge case:

```markdown
## AI-Generated Tests

### Test 1: Empty Input

**Purpose**: Verify behavior with no data
**Input**: []
**Expected Output**: []
**Rationale**: [Why this case matters]

### Test 2: Single Element

**Purpose**: Verify minimum valid input
**Input**: [1]
**Expected Output**: [1]
**Rationale**: [Why this case matters]

### Test 3: Maximum Size

**Purpose**: Verify performance at scale
**Input**: [1..10000]
**Expected Output**: [sorted result]
**Rationale**: [Why this case matters]
```

## Test Anchoring Flow

```
Initial State:
  anchor_tests = []
  pending_tests = [public_tests + ai_tests]

For each code iteration:
  1. Run anchor_tests
     - If ANY fail → REVERT changes, go to REFLECTOR
     - If ALL pass → continue

  2. Run pending_tests
     - For each passing test:
       - Move to anchor_tests (immutable now)
     - For each failing test:
       - Keep in pending_tests
       - Analyze failure

  3. If all pending_tests pass:
     - Done! All tests are now anchors

  4. If some pending_tests fail:
     - Fix code (without breaking anchors)
     - Repeat from step 1
```

## Key Insight: Monotonic Progress

The anchor system ensures:

- **No Regressions**: Can't break what's working
- **Clear Progress**: Anchor count only increases
- **Safe Iteration**: Each fix is validated against all previous fixes

## Integration with imlazy

| imlazy Node | AlphaCodium Phase                       |
| ----------- | --------------------------------------- |
| PLANNER     | Problem Reflection, Solution Generation |
| REASONER    | Solution Selection, Test Design         |
| CODER       | Implementation, Test Anchoring          |
| VERIFIER    | Final Test Execution                    |
| REFLECTOR   | Failure Analysis, Iteration             |

## Example Flow

```
Input: "Sort array in descending order"

PLANNER:
  - Goal: Sort array descending
  - Edge cases: empty, single, duplicates, already sorted
  - Solutions: A) reverse sort, B) custom comparator
  - Selected: A (simpler)

REASONER:
  - ToT: Confirm approach handles all edge cases
  - Plan: 1) Implement, 2) Test edges, 3) Verify

CODER:
  - Write sort function
  - Run tests: empty ✓ → anchor
  - Run tests: single ✓ → anchor
  - Run tests: duplicates ✗ → fix
  - Run tests: duplicates ✓ → anchor

VERIFIER:
  - All 4 anchors pass
  - Coverage complete

CONSOLIDATOR:
  - Archive solution
  - Store "descending sort" pattern
```
