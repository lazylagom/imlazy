---
name: Code Analysis
description: This skill should be used when the user asks to "analyze code", "understand codebase", "find patterns", "assess impact", "explore code structure", or needs guidance on code exploration, pattern recognition, or codebase understanding techniques.
version: 0.1.0
---

# Code Analysis

## Overview

Code analysis involves exploring and understanding existing code to inform development decisions. Effective analysis prevents reinventing the wheel and ensures new code integrates smoothly.

## Core Principles

1. **Read Before Write**: Understand existing patterns before adding new code
2. **Follow Conventions**: Match the codebase's existing style
3. **Minimize Impact**: Identify the smallest change footprint
4. **Leverage Existing**: Reuse existing utilities and patterns

## Analysis Process

### Step 1: Project Structure Discovery

Explore the project layout:

```bash
# Find project structure
ls -la
find . -type f -name "*.ts" | head -20

# Identify key directories
# - src/, lib/ - Source code
# - tests/, __tests__ - Tests
# - config/, settings - Configuration
# - types/, interfaces - Type definitions
```

### Step 2: Entry Point Identification

Find main entry points:
- `main.ts`, `index.ts`, `app.ts`
- `package.json` scripts
- Configuration files

### Step 3: Pattern Recognition

Identify coding patterns used:

**Architecture Patterns:**
- MVC, MVVM, Clean Architecture
- Microservices, Monolith
- Event-driven, Request-response

**Code Patterns:**
- Repository pattern
- Factory pattern
- Dependency injection
- Middleware pattern

### Step 4: Dependency Mapping

Trace dependencies:
- Internal imports
- External packages
- Shared utilities
- Type definitions

### Step 5: Impact Assessment

Evaluate change impact:

```markdown
## Impact Assessment
| File | Type | Risk Level | Reason |
|------|------|------------|--------|
| path/file.ts | Modify | High | Core logic |
| path/util.ts | Add | Low | New utility |
```

## Search Strategies

### Finding Relevant Code

```bash
# Find files by name pattern
glob "**/*.service.ts"

# Search for specific patterns
grep -r "class.*Controller"
grep -r "function handle"

# Find usages
grep -r "functionName"
```

### Understanding Data Flow

1. Find where data enters (API endpoints, event handlers)
2. Trace through processing logic
3. Identify where data persists or exits
4. Map error handling paths

### Finding Similar Implementations

Search for analogous features:
- Similar file names
- Related test files
- Documentation references

## Analysis Output Template

```markdown
# Code Analysis Report

## Project Overview
- **Type**: [Web app, CLI, library, etc.]
- **Language**: [Primary language and framework]
- **Structure**: [Architecture pattern]

## Relevant Files

| File | Purpose | Relevance |
|------|---------|-----------|
| path/to/file | Description | High/Medium/Low |

## Patterns Identified

### Coding Conventions
- Naming: [camelCase, snake_case, etc.]
- File structure: [Description]
- Error handling: [Approach]

### Architecture Patterns
- [Pattern name]: [How it's used]

## Dependencies

### Internal
- [Module 1]: [Purpose]

### External
- [Package 1]: [Purpose]

## Impact Analysis

### Files to Modify
1. `file.ts`: [What changes]

### Files to Create
1. `new-file.ts`: [Purpose]

### Potential Risks
- [Risk 1]

## Recommendations
- [Recommendation based on analysis]
```

## Common Analysis Scenarios

### Adding a New Feature
1. Find similar features
2. Identify integration points
3. Note required imports
4. Map test file locations

### Fixing a Bug
1. Reproduce the bug path
2. Trace the code flow
3. Identify the fault location
4. Find related test coverage

### Refactoring
1. Map all usages
2. Identify breaking change risk
3. Find dependent code
4. Plan migration path

## Quality Checklist

Before completing analysis:
- [ ] Key files identified
- [ ] Patterns documented
- [ ] Dependencies mapped
- [ ] Impact assessed
- [ ] Similar implementations found
- [ ] Risks identified
- [ ] Recommendations provided
