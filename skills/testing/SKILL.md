---
name: Testing
description: This skill should be used when the user asks to "write tests", "create test cases", "test coverage", "unit testing", "integration testing", "TDD", or needs guidance on testing strategies, test design, or quality assurance practices.
version: 0.1.0
---

# Testing

## Overview

Testing ensures code works correctly and continues to work as it evolves. Good tests catch bugs early, document behavior, and enable confident refactoring.

## Core Principles

1. **Test Behavior, Not Implementation**: Tests should verify what code does, not how
2. **Isolation**: Each test should be independent
3. **Readability**: Tests are documentation
4. **Speed**: Tests should run fast
5. **Reliability**: Tests should never be flaky

## Testing Pyramid

```
    /\
   /  \  E2E Tests (few, slow, broad)
  /----\
 /      \  Integration Tests (some, medium)
/--------\
/          \  Unit Tests (many, fast, focused)
```

### Unit Tests
- Test individual functions/classes
- Mock external dependencies
- Fast execution
- High coverage

### Integration Tests
- Test component interactions
- Use real dependencies when practical
- Test critical paths
- Medium coverage

### E2E Tests
- Test complete user flows
- Full system testing
- Slow but comprehensive
- Low coverage, high value

## Test Structure

### AAA Pattern

```typescript
describe('Calculator', () => {
  describe('add', () => {
    it('should add two positive numbers', () => {
      // Arrange
      const calc = new Calculator();

      // Act
      const result = calc.add(2, 3);

      // Assert
      expect(result).toBe(5);
    });
  });
});
```

### Test Naming

```typescript
// Format: should [expected behavior] when [condition]
it('should return empty array when input is empty', () => {});
it('should throw ValidationError when email is invalid', () => {});
it('should retry 3 times when service fails', () => {});
```

## Test Patterns

### Testing Async Code

```typescript
// Using async/await
it('should fetch user data', async () => {
  const user = await userService.getUser('123');
  expect(user.name).toBe('John');
});

// Testing rejections
it('should throw when user not found', async () => {
  await expect(userService.getUser('invalid'))
    .rejects.toThrow('User not found');
});
```

### Mocking

```typescript
// Mock external dependencies
const mockDb = {
  find: jest.fn().mockResolvedValue({ id: '1', name: 'Test' }),
  save: jest.fn().mockResolvedValue(undefined),
};

const service = new UserService(mockDb);

it('should call db.find with correct id', async () => {
  await service.getUser('123');
  expect(mockDb.find).toHaveBeenCalledWith('123');
});
```

### Testing Error Handling

```typescript
it('should handle validation errors', async () => {
  const result = await service.process({ invalid: 'data' });

  expect(result.success).toBe(false);
  expect(result.error).toContain('validation');
});

it('should throw for network failures', async () => {
  mockApi.get.mockRejectedValue(new NetworkError());

  await expect(service.fetch())
    .rejects.toThrow('Service unavailable');
});
```

### Parameterized Tests

```typescript
describe('isValidEmail', () => {
  const testCases = [
    { input: 'test@example.com', expected: true },
    { input: 'invalid', expected: false },
    { input: '', expected: false },
    { input: 'a@b.c', expected: true },
  ];

  testCases.forEach(({ input, expected }) => {
    it(`should return ${expected} for "${input}"`, () => {
      expect(isValidEmail(input)).toBe(expected);
    });
  });
});
```

## Test Coverage Areas

### Happy Path
- Normal expected inputs
- Successful operations
- Valid data flows

### Edge Cases
- Empty inputs
- Null/undefined values
- Boundary values
- Maximum/minimum values

### Error Cases
- Invalid inputs
- Missing required data
- External failures
- Timeout scenarios

### Security Cases
- Injection attempts
- Authorization failures
- Invalid tokens

## Test File Organization

```
src/
├── user/
│   ├── user.service.ts
│   └── __tests__/
│       ├── user.service.test.ts
│       └── user.service.integration.test.ts
├── order/
│   ├── order.processor.ts
│   └── __tests__/
│       └── order.processor.test.ts
└── test/
    ├── fixtures/
    │   └── users.json
    ├── helpers/
    │   └── test-utils.ts
    └── setup.ts
```

## Test Utilities

### Test Factories

```typescript
// Create test data easily
function createTestUser(overrides = {}): User {
  return {
    id: 'test-id',
    email: 'test@example.com',
    name: 'Test User',
    ...overrides,
  };
}

it('should update user name', async () => {
  const user = createTestUser({ name: 'Original' });
  // ...
});
```

### Custom Matchers

```typescript
// Extend expect for domain-specific assertions
expect.extend({
  toBeValidEmail(received) {
    const pass = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(received);
    return {
      pass,
      message: () => `expected ${received} to be a valid email`,
    };
  },
});

expect('test@example.com').toBeValidEmail();
```

## Common Testing Mistakes

### Avoid These

```typescript
// ❌ Testing implementation details
expect(service._internalMethod).toHaveBeenCalled();

// ❌ Flaky tests with timing
await delay(1000); // Hope it's done

// ❌ Tests that depend on order
it('first test sets global state');
it('second test relies on that state');

// ❌ Too many assertions per test
it('should do everything', () => {
  expect(a).toBe(1);
  expect(b).toBe(2);
  expect(c).toBe(3);
  // ... 20 more assertions
});
```

## Quality Checklist

Before completing tests:
- [ ] Happy path covered
- [ ] Edge cases tested
- [ ] Error handling verified
- [ ] Tests are independent
- [ ] Test names are descriptive
- [ ] No flaky tests
- [ ] Tests run fast
- [ ] Mock external dependencies
- [ ] Coverage meets threshold
- [ ] Tests are maintainable
