# JVIS Test Suite

## Structure

```
tests/
├── unit/           # Unit tests for individual components
│   └── lib/        # Shell library tests
├── integration/    # Integration tests
├── smoke/          # Quick smoke tests for CI
└── fixtures/       # Test fixtures and mock data
    ├── sample_project/
    └── mock_configs/
```

## Running Tests

### Smoke Tests (Quick)
```bash
./tests/smoke/test_cli.sh
./tests/smoke/test_agents.sh
```

### All Tests
```bash
./tests/run_all.sh
```

## Writing Tests

### Shell Tests
- Use `set -euo pipefail` at the top
- Define `fail()` function for assertions
- Exit 0 on success, non-zero on failure

### Python Tests
- Use pytest
- Follow naming: `test_*.py`
- Use fixtures for common setup
