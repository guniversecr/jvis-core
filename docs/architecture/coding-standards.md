# Coding Standards

Code standards for projects generated with JVIS.

---

## Indentation and Formatting

### By Language (defined in EditorConfig)

| Language | Indent | Style |
|----------|--------|-------|
| Python | 4 spaces | PEP 8 |
| JavaScript/TypeScript | 2 spaces | Prettier |
| YAML/JSON | 2 spaces | - |
| Makefile | Tabs | - |

### Line Length
- **Python**: 100 characters (Black default)
- **JavaScript/TypeScript**: 100 characters (Prettier)

---

## Tooling by Language

### Python
```bash
# Formatting
black src/ tests/

# Linting (replaces flake8, faster)
ruff src/ tests/

# Type checking
mypy src/

# Testing
pytest --cov=src
```

### JavaScript/TypeScript
```bash
# Formatting
yarn prettier --write .

# Linting
yarn eslint --fix .

# Type checking
yarn tsc --noEmit

# Testing
yarn test
```

---

## Naming Conventions

### Variables and Functions

**Python (snake_case):**
```python
# Variables
user_name = "John"
is_active = True
user_list = []

# Functions
def get_user_by_id(user_id: int) -> User:
    pass

def validate_email(email: str) -> bool:
    pass
```

**JavaScript/TypeScript (camelCase):**
```typescript
// Variables
const userName = "John";
const isActive = true;
const userList: User[] = [];

// Functions
function getUserById(userId: number): User {
  // ...
}

const validateEmail = (email: string): boolean => {
  // ...
};
```

### Classes (PascalCase in both)
```python
# Python
class UserService:
    pass

class PaymentProcessor:
    pass
```

```typescript
// TypeScript
class UserService {}
class PaymentProcessor {}
```

### Constants (UPPER_SNAKE_CASE)
```python
MAX_RETRY_ATTEMPTS = 3
DEFAULT_TIMEOUT_SECONDS = 30
```

```typescript
const MAX_RETRY_ATTEMPTS = 3;
const DEFAULT_TIMEOUT_SECONDS = 30;
```

---

## Comments

```python
# Good - Explains the WHY, not the WHAT
# We use cache to avoid expensive DB queries
cached_data = get_from_cache(key)

# Bad - States the obvious
# Get data from cache
cached_data = get_from_cache(key)
```

---

## Error Handling

### Python
```python
# Good
try:
    result = risky_operation()
except SpecificError as e:
    logger.error(f"Operation failed: {e}")
    raise CustomError("User-friendly message") from e

# Bad
try:
    result = risky_operation()
except Exception as e:
    print(e)
```

### TypeScript
```typescript
// Good
try {
  const result = await riskyOperation();
} catch (error) {
  logger.error('Operation failed:', error);
  throw new CustomError('User-friendly message');
}

// Bad
try {
  const result = await riskyOperation();
} catch (e) {
  console.log(e);
}
```

---

## Async/Await

### Python
```python
# Good (FastAPI)
async def fetch_user_data(user_id: int) -> dict:
    user = await user_service.get_user(user_id)
    posts = await post_service.get_user_posts(user_id)
    return {"user": user, "posts": posts}
```

### TypeScript
```typescript
// Good
async function fetchUserData(userId: number) {
  const user = await userService.getUser(userId);
  const posts = await postService.getUserPosts(userId);
  return { user, posts };
}

// Bad - callback hell
function fetchUserData(userId: number) {
  return userService.getUser(userId).then(user => {
    return postService.getUserPosts(userId).then(posts => {
      return { user, posts };
    });
  });
}
```

---

## Testing Standards

### Coverage
- **Minimum**: 80% on critical paths
- **Ideal**: 90%+ on business logic

### Test Names
```python
# Python - descriptive
def test_should_return_error_when_email_is_invalid():
    # ...

def test_user_creation_with_valid_data_succeeds():
    # ...
```

```typescript
// TypeScript - descriptive
test('should return error when email is invalid', () => {
  // ...
});

describe('UserService', () => {
  it('creates user with valid data', async () => {
    // ...
  });
});
```

---

## Pre-commit Hooks

All projects include pre-commit configured:

```bash
# Install (once)
pip install pre-commit
pre-commit install

# Runs automatically on every commit
# Or manually:
pre-commit run --all-files
```

**Python hooks:** Black, Ruff, MyPy, detect-secrets
**JS/TS hooks:** ESLint, Prettier, TSC, detect-secrets

---

## General Principles

1. **DRY** - Don't Repeat Yourself
2. **KISS** - Keep It Simple, Stupid
3. **YAGNI** - You Aren't Gonna Need It
4. **Single Responsibility** - One function, one purpose
5. **Explicit over Implicit** - Clear code over "clever" code
