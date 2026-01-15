---
name: Implementation
description: This skill should be used when the user asks to "implement feature", "write code", "coding best practices", "write clean code", "refactor code", or needs guidance on software implementation, coding standards, or development best practices.
version: 0.1.0
---

# Implementation

## Overview

Implementation turns designs into working code. Quality implementation is readable, maintainable, and thoroughly tested.

## Core Principles

1. **Readability First**: Code is read more than written
2. **Single Responsibility**: Each unit does one thing well
3. **DRY**: Don't Repeat Yourself
4. **YAGNI**: Don't build what's not needed yet
5. **Fail Fast**: Validate early, fail with clear messages

## Implementation Process

### Step 1: Setup

Before coding:
- Review design document
- Create necessary files/directories
- Set up test files alongside
- Create TODO list for tracking

### Step 2: Skeleton First

Build structure before details:

```typescript
// Start with interface/types
interface OrderProcessor {
  process(order: Order): Promise<Result>;
}

// Then implement with stubs
class OrderProcessorImpl implements OrderProcessor {
  async process(order: Order): Promise<Result> {
    // TODO: Implement validation
    // TODO: Implement processing logic
    // TODO: Implement persistence
    throw new Error('Not implemented');
  }
}
```

### Step 3: Test-Driven Development

Write tests alongside code:

```typescript
// Write test first
describe('OrderProcessor', () => {
  it('should process valid order', async () => {
    const processor = new OrderProcessorImpl();
    const result = await processor.process(validOrder);
    expect(result.success).toBe(true);
  });
});

// Then implement to pass
```

### Step 4: Incremental Implementation

Build in small, testable increments:
1. Implement one function
2. Write/run its tests
3. Refactor if needed
4. Move to next function

### Step 5: Error Handling

Handle failures gracefully:

```typescript
// Input validation
function processOrder(order: Order): Result {
  if (!order.items?.length) {
    throw new ValidationError('Order must have items');
  }
  // ...
}

// External failures
try {
  await externalService.call();
} catch (error) {
  logger.error('External service failed', error);
  throw new ServiceError('Unable to process order');
}
```

## Coding Standards

### Naming Conventions

```typescript
// Variables: camelCase, descriptive
const userEmail = 'test@example.com';
const isActive = true;

// Functions: verb + noun
function calculateTotal() {}
function validateInput() {}
function handleError() {}

// Classes: PascalCase, noun
class OrderProcessor {}
class UserService {}

// Constants: UPPER_SNAKE_CASE
const MAX_RETRY_COUNT = 3;
const DEFAULT_TIMEOUT = 5000;
```

### Function Design

```typescript
// Small, focused functions (< 20 lines ideal)
function validateEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

// Clear parameters and return types
function createUser(
  email: string,
  name: string,
  options?: CreateUserOptions
): Promise<User> {
  // ...
}

// Prefer pure functions when possible
function calculateDiscount(price: number, rate: number): number {
  return price * rate;
}
```

### Error Handling Patterns

```typescript
// Custom error types
class ValidationError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'ValidationError';
  }
}

// Result pattern for expected failures
type Result<T> =
  | { success: true; data: T }
  | { success: false; error: string };

// Proper async error handling
async function fetchData(): Promise<Data> {
  try {
    const response = await api.get('/data');
    return response.data;
  } catch (error) {
    if (error instanceof NetworkError) {
      throw new ServiceUnavailableError('API unreachable');
    }
    throw error;
  }
}
```

## Code Organization

### File Structure

```
src/
├── features/
│   └── orders/
│       ├── order.service.ts
│       ├── order.types.ts
│       ├── order.utils.ts
│       └── __tests__/
│           └── order.service.test.ts
├── shared/
│   ├── utils/
│   └── types/
└── index.ts
```

### Module Design

```typescript
// Export public interface only
// order.service.ts
export class OrderService {
  // Public methods
  async createOrder(data: CreateOrderData): Promise<Order> {}
  async getOrder(id: string): Promise<Order> {}
}

// Internal helpers stay private
function validateOrderData(data: CreateOrderData): void {}
```

## Testing Guidelines

### Test Structure

```typescript
describe('OrderService', () => {
  describe('createOrder', () => {
    it('should create order with valid data', async () => {
      // Arrange
      const data = { items: [{ id: '1', quantity: 2 }] };

      // Act
      const result = await service.createOrder(data);

      // Assert
      expect(result.id).toBeDefined();
      expect(result.items).toHaveLength(1);
    });

    it('should throw for empty items', async () => {
      const data = { items: [] };
      await expect(service.createOrder(data))
        .rejects.toThrow('Order must have items');
    });
  });
});
```

### Test Coverage Goals

- Unit tests: All public functions
- Integration tests: Key workflows
- Edge cases: Empty inputs, nulls, boundaries

## Quality Checklist

Before completing implementation:
- [ ] Code follows project conventions
- [ ] Functions are small and focused
- [ ] Error handling is complete
- [ ] Input validation present
- [ ] Tests cover happy path
- [ ] Tests cover error cases
- [ ] No hardcoded values
- [ ] Logging added where appropriate
- [ ] No lint errors
- [ ] Code is self-documenting
