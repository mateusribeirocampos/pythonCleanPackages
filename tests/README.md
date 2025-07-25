# Tests Directory

This directory is prepared for future test implementations for the Python Clean Packages toolkit.

## Planned Test Structure

```
tests/
├── __init__.py
├── README.md (this file)
├── test_cleanup_packages.py    # Tests for cleanup_packages.py
├── test_check_packages.py      # Tests for check_packages.sh functionality
├── test_integration.py         # Integration tests
└── fixtures/                   # Test fixtures and mock data
    ├── mock_environments/
    └── sample_packages.json
```

## Testing Framework Recommendations

### For Python Scripts (`cleanup_packages.py`)
- **pytest**: Modern, feature-rich testing framework
- **unittest.mock**: For mocking pip commands and system calls
- **tempfile**: For creating temporary environments during tests

### For Shell Scripts (`check_packages.sh`)
- **bats**: Bash Automated Testing System
- **shellcheck**: Static analysis for shell scripts

## Sample Test Commands (Future)

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_cleanup_packages.py

# Run with coverage
pytest --cov=scripts tests/

# Run shell script tests (when implemented)
bats tests/test_check_packages.bats
```

## Test Categories to Implement

### Unit Tests
- Package detection logic
- Protected package identification
- Environment detection
- Command parsing

### Integration Tests  
- Full cleanup workflow
- Cross-platform compatibility
- Virtual environment interactions

### Safety Tests
- Ensure protected packages are never removed
- Verify environment isolation
- Test dry-run mode accuracy

## Mock Testing Scenarios

### Virtual Environment Mocking
- Simulate different virtual environment states
- Mock pip list outputs
- Test environment switching

### Package List Mocking
- Various package configurations
- Different Python versions
- Platform-specific packages

## Contributing Tests

When adding tests:
1. Follow existing naming conventions
2. Include both positive and negative test cases
3. Mock external dependencies (pip, subprocess)
4. Test error handling and edge cases
5. Ensure tests are platform-independent where possible

## Test Data

Tests should include realistic package scenarios:
- Clean virtual environments
- Messy development environments  
- Global system environments
- Mixed package installations