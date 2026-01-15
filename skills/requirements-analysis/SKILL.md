---
name: Requirements Analysis
description: This skill should be used when the user asks to "analyze requirements", "clarify scope", "define acceptance criteria", "break down user story", "gather requirements", or needs guidance on requirements gathering, scope definition, or requirements documentation best practices.
version: 0.1.0
---

# Requirements Analysis

## Overview

Requirements analysis is the process of understanding what needs to be built before implementation begins. Effective requirements analysis prevents costly rework and ensures alignment between stakeholders.

## Core Principles

1. **Clarity over Assumption**: Never assume; always clarify ambiguous requirements
2. **Completeness**: Identify all requirements, including implicit ones
3. **Testability**: Every requirement should have verifiable acceptance criteria
4. **Priority**: Distinguish must-haves from nice-to-haves

## Requirements Gathering Process

### Step 1: Initial Understanding

Read the task description carefully. Identify:
- The primary goal
- Key stakeholders
- Constraints mentioned
- Implicit requirements

### Step 2: Functional Requirements

Extract what the system must do:

```markdown
## Functional Requirements
| ID | Description | Priority | Acceptance Criteria |
|----|-------------|----------|---------------------|
| FR-1 | [What the system does] | Must/Should/Could | [How to verify] |
```

**Priority Levels (MoSCoW):**
- **Must**: Critical for success
- **Should**: Important but not critical
- **Could**: Nice to have
- **Won't**: Out of scope (this version)

### Step 3: Non-Functional Requirements

Identify quality attributes:

- **Performance**: Response times, throughput
- **Security**: Authentication, authorization, data protection
- **Scalability**: Expected growth, load handling
- **Usability**: User experience requirements
- **Reliability**: Uptime, error handling
- **Maintainability**: Code quality, documentation

### Step 4: Constraint Identification

Document limitations:
- Technical constraints (languages, frameworks, infrastructure)
- Business constraints (timeline, budget, regulations)
- Integration constraints (existing systems, APIs)

### Step 5: Gap Analysis

Identify missing information:
- Questions that need answers
- Assumptions being made
- Decisions pending

## Requirements Documentation Template

```markdown
# Requirements Document

## 1. Overview
[Brief description of what needs to be built]

## 2. Goals
- Primary: [Main objective]
- Secondary: [Supporting objectives]

## 3. Functional Requirements
| ID | Requirement | Priority | Acceptance Criteria |
|----|-------------|----------|---------------------|

## 4. Non-Functional Requirements
| Category | Requirement | Metric |
|----------|-------------|--------|

## 5. Constraints
- [Constraint 1]
- [Constraint 2]

## 6. Assumptions
- [Assumption 1]
- [Assumption 2]

## 7. Open Questions
- [Question 1]
- [Question 2]

## 8. Out of Scope
- [Item 1]
- [Item 2]
```

## User Story Format

When breaking down into user stories:

```
As a [type of user]
I want [goal/desire]
So that [benefit/value]

Acceptance Criteria:
- Given [context], when [action], then [outcome]
```

## Common Patterns

### Feature Request Analysis
1. Identify the core value proposition
2. Break into smaller deliverables
3. Define MVP vs full feature
4. Identify dependencies

### Bug Fix Analysis
1. Understand current behavior
2. Define expected behavior
3. Identify root cause location
4. Define verification steps

### Refactoring Analysis
1. Identify pain points
2. Define target state
3. Assess risk and impact
4. Define success criteria

## Quality Checklist

Before completing requirements:
- [ ] All functional requirements identified
- [ ] Non-functional requirements considered
- [ ] Acceptance criteria are testable
- [ ] Priorities assigned
- [ ] Assumptions documented
- [ ] Open questions listed
- [ ] Scope clearly defined
