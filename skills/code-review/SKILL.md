---
name: Code Review
description: This skill should be used when the user asks to "review code", "check code quality", "find bugs", "security review", "code feedback", or needs guidance on code review practices, quality assessment, or identifying code issues.
version: 0.1.0
---

# Code Review

## Overview

Code review ensures code quality, catches bugs, shares knowledge, and maintains consistency. Effective reviews balance thoroughness with constructiveness.

## Core Principles

1. **Constructive Feedback**: Critique code, not the author
2. **Focus on Significance**: Prioritize important issues over style nitpicks
3. **Explain Why**: Provide reasoning, not just criticism
4. **Suggest Solutions**: Offer alternatives when possible
5. **Acknowledge Good Work**: Recognize quality patterns

## Review Process

### Step 1: Understand Context

Before reviewing:
- Read the requirements/ticket
- Understand the goal
- Review any design documents
- Check previous context from analysis

### Step 2: High-Level Review

First pass - overall assessment:
- Does it solve the stated problem?
- Is the approach reasonable?
- Are there major architectural concerns?

### Step 3: Detailed Review

Second pass - line by line:
- Logic correctness
- Edge case handling
- Error handling
- Code quality
- Testing coverage

### Step 4: Security Review

Check for vulnerabilities:
- Input validation
- Authentication/authorization
- Data exposure
- Injection risks

### Step 5: Summarize Findings

Organize feedback by severity and provide actionable recommendations.

## Review Checklist

### Correctness
- [ ] Logic is correct
- [ ] Edge cases handled
- [ ] Null/undefined checks present
- [ ] Error handling complete
- [ ] Async operations handled properly

### Code Quality
- [ ] Readable and understandable
- [ ] Functions are focused and small
- [ ] Naming is clear and consistent
- [ ] No code duplication
- [ ] Comments explain "why" not "what"

### Security
- [ ] Input is validated
- [ ] No sensitive data exposed
- [ ] Auth checks in place
- [ ] No injection vulnerabilities
- [ ] Secrets not hardcoded

### Testing
- [ ] Unit tests for new logic
- [ ] Edge cases tested
- [ ] Error paths tested
- [ ] Tests are maintainable

### Performance
- [ ] No obvious inefficiencies
- [ ] Database queries optimized
- [ ] No unnecessary loops
- [ ] Memory usage reasonable

### Maintainability
- [ ] Follows project patterns
- [ ] Dependencies justified
- [ ] Configuration not hardcoded
- [ ] Documentation updated

## Severity Levels

### Critical (Must Fix)
- Security vulnerabilities
- Data loss risks
- Breaking functionality
- Production blockers

### High (Should Fix)
- Logic errors
- Missing error handling
- Performance issues
- Test gaps for critical paths

### Medium (Recommended)
- Code quality issues
- Minor edge cases
- Readability improvements
- Test coverage gaps

### Low (Optional)
- Style preferences
- Minor optimizations
- Documentation suggestions
- Nice-to-have improvements

## Feedback Format

### Issue Template

```markdown
**Severity**: [Critical/High/Medium/Low]
**Location**: `file.ts:42`
**Issue**: [Description of the problem]
**Suggestion**: [How to fix it]
```

### Positive Feedback

```markdown
**Good**: Clean use of the factory pattern here. Makes testing much easier.
**Good**: Excellent error handling - all edge cases covered.
```

## Common Issues to Look For

### Logic Issues
- Off-by-one errors in loops
- Wrong comparison operators (= vs ===)
- Missing await in async functions
- Incorrect null/undefined handling

### Security Issues
- SQL injection via string concatenation
- XSS via unsanitized user input
- Exposed secrets in code
- Missing authentication checks

### Error Handling Issues
- Swallowed exceptions
- Missing validation
- Unclear error messages
- Unhandled promise rejections

### Performance Issues
- N+1 database queries
- Unnecessary work in loops
- Missing caching opportunities
- Large synchronous operations

## Review Summary Template

```markdown
# Code Review Summary

## Overall Assessment
**Verdict**: [Approve / Request Changes / Needs Discussion]
**Quality Score**: [1-10]

## Requirements Check
| Requirement | Status | Notes |
|-------------|--------|-------|
| FR-1 | Met | |
| FR-2 | Partial | Missing edge case |

## Issues Found

### Critical
[None / List items]

### High
1. **[file:line]**: [Issue and fix]

### Medium
1. **[file:line]**: [Issue and fix]

### Low
1. **[file:line]**: [Issue and fix]

## Positive Observations
- [Good pattern usage]
- [Clean implementation]

## Recommendations
1. [Key recommendation]
2. [Secondary recommendation]
```

## Quality Checklist

Before completing review:
- [ ] Understood requirements context
- [ ] Verified correctness
- [ ] Checked security concerns
- [ ] Assessed code quality
- [ ] Reviewed test coverage
- [ ] Prioritized issues by severity
- [ ] Provided actionable feedback
- [ ] Acknowledged good work
- [ ] Summary is clear and constructive
