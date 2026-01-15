---
name: System Design
description: This skill should be used when the user asks to "design architecture", "plan implementation", "create system design", "choose patterns", "design API", or needs guidance on software architecture, design patterns, or technical decision-making.
version: 0.1.0
---

# System Design

## Overview

System design translates requirements into a technical blueprint. Good design balances immediate needs with future flexibility while staying aligned with existing codebase patterns.

## Core Principles

1. **Simplicity First**: Choose the simplest solution that works
2. **Consistency**: Match existing patterns in the codebase
3. **Separation of Concerns**: Clear boundaries between components
4. **Testability**: Design for easy testing
5. **Extensibility**: Allow for future changes without rewrites

## Design Process

### Step 1: Review Inputs

Before designing, gather:
- Requirements analysis output
- Code analysis findings
- Existing patterns to follow
- Constraints to respect

### Step 2: High-Level Design

Define the overall approach:

```markdown
## Solution Overview
[One paragraph describing the approach]

## Component Diagram
```
[Component A] -> [Component B] -> [Component C]
       |              |
       v              v
   [Store]       [External API]
```
```

### Step 3: Component Design

For each component:

```markdown
## Component: [Name]

### Purpose
[What this component does]

### Interface
- Input: [What it receives]
- Output: [What it returns]
- Side effects: [External changes]

### Dependencies
- [Dependency 1]
- [Dependency 2]

### Key Decisions
- [Decision and rationale]
```

### Step 4: Data Model Design

Define data structures:

```typescript
// Example data model
interface User {
  id: string;
  email: string;
  createdAt: Date;
}
```

Consider:
- Required vs optional fields
- Relationships between entities
- Validation rules
- Serialization format

### Step 5: API/Interface Design

Define contracts:

```typescript
// Function signature
function processOrder(order: Order): Promise<Result>;

// API endpoint
POST /api/orders
Body: { items: Item[], userId: string }
Response: { orderId: string, status: string }
```

### Step 6: Error Handling Design

Plan for failures:
- Input validation errors
- Business logic errors
- External service failures
- Unexpected errors

## Design Patterns Reference

### Creational Patterns
- **Factory**: Create objects without specifying exact class
- **Builder**: Construct complex objects step by step
- **Singleton**: Ensure single instance

### Structural Patterns
- **Adapter**: Convert interface to another
- **Decorator**: Add behavior dynamically
- **Facade**: Simplify complex subsystem

### Behavioral Patterns
- **Strategy**: Define family of algorithms
- **Observer**: Notify dependents of changes
- **Command**: Encapsulate request as object

## Design Document Template

```markdown
# Design Document: [Feature Name]

## 1. Overview
[Brief description]

## 2. Goals
- [Goal 1]
- [Goal 2]

## 3. Non-Goals
- [What this design doesn't address]

## 4. Design

### 4.1 Component Architecture
[Diagram and description]

### 4.2 Data Model
[Data structures]

### 4.3 API Design
[Interfaces and contracts]

### 4.4 Key Algorithms
[Important logic]

## 5. Implementation Plan

### Phase 1: [Name]
- [ ] Task 1
- [ ] Task 2

### Phase 2: [Name]
- [ ] Task 1

## 6. Testing Strategy
- Unit: [Approach]
- Integration: [Approach]

## 7. Security Considerations
- [Consideration 1]

## 8. Performance Considerations
- [Consideration 1]

## 9. Trade-offs
| Option | Pros | Cons | Decision |
|--------|------|------|----------|

## 10. Open Questions
- [Question 1]
```

## Decision Framework

When choosing between options:

1. **List Options**: Identify all viable approaches
2. **Define Criteria**: What matters (performance, simplicity, cost)
3. **Evaluate**: Score each option against criteria
4. **Document**: Record decision and rationale

```markdown
## Decision: [Topic]

### Options Considered
1. [Option A]: [Description]
2. [Option B]: [Description]

### Evaluation
| Criteria | Option A | Option B |
|----------|----------|----------|
| Simplicity | High | Medium |
| Performance | Medium | High |

### Decision
[Choice] because [rationale]
```

## Quality Checklist

Before completing design:
- [ ] Aligns with requirements
- [ ] Matches existing patterns
- [ ] Components clearly defined
- [ ] Interfaces specified
- [ ] Data models designed
- [ ] Error handling planned
- [ ] Testing strategy defined
- [ ] Trade-offs documented
