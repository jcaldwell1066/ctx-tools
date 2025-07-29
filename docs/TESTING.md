# Testing Standards for CTX-Tools

This document outlines the comprehensive testing strategy for the ctx-tools project, covering unit tests, integration tests, and multimodal synchronization testing.

## Testing Philosophy

Our testing approach follows these principles:

1. **Comprehensive Coverage**: Test core functionality, CLI commands, MCP integration, and cross-interface synchronization
2. **Fast Feedback**: Unit tests run quickly, integration tests are thorough, multimodal tests verify real-world scenarios
3. **Regression Prevention**: Specific tests for bugs we've fixed to prevent regressions
4. **Real-world Scenarios**: Tests mirror actual usage patterns

## Test Structure

```
tests/
├── conftest.py              # Shared fixtures and configuration
├── unit/                    # Fast unit tests for core functionality
│   ├── test_models.py       # Context, Note, ContextState tests
│   └── test_core.py         # ContextManager tests
├── integration/             # CLI and component integration tests
│   ├── test_cli_integration.py    # CLI command tests
│   └── test_mcp_integration.py    # MCP server tests
└── multimodal/              # Cross-interface synchronization tests
    └── test_sync.py         # CLI ↔ MCP sync verification
```

## Test Categories

### Unit Tests (`@pytest.mark.unit`)

**Purpose**: Test individual components in isolation  
**Speed**: Very fast (< 1s each)  
**Coverage**: Core business logic

**Examples**:
- Context creation and state management
- Note addition and retrieval
- Context stack operations
- Data serialization/deserialization

```bash
# Run only unit tests
pytest -m unit
```

### Integration Tests (`@pytest.mark.integration`)

**Purpose**: Test component interactions and CLI commands  
**Speed**: Moderate (1-5s each)  
**Coverage**: CLI commands, error handling, edge cases

**Examples**:
- CLI command execution
- File I/O operations
- Error handling scenarios
- Command routing

```bash
# Run only integration tests  
pytest -m integration
```

### MCP Integration Tests (`@pytest.mark.mcp`)

**Purpose**: Test MCP server functionality  
**Speed**: Moderate (2-10s each)  
**Coverage**: MCP protocol compliance, tool execution

**Examples**:
- MCP server initialization
- Tool discovery and execution
- Protocol compliance
- Error handling

```bash
# Run only MCP tests
pytest -m mcp
```

### Multimodal Tests (`@pytest.mark.multimodal`)

**Purpose**: Test CLI-MCP synchronization  
**Speed**: Slower (5-15s each)  
**Coverage**: Cross-interface data consistency

**Examples**:
- State changes sync between CLI and MCP
- Context creation consistency
- Bidirectional data flow
- Regression prevention

```bash
# Run only multimodal tests
pytest -m multimodal
```

## Running Tests

### Quick Development Cycle
```bash
# Fast unit tests only
pytest -m unit

# Unit tests with coverage
pytest -m unit --cov=ctx --cov-report=term-missing
```

### Pre-commit Testing
```bash
# Core functionality (unit + integration)
pytest -m "unit or integration" --cov=ctx

# Skip slow tests
pytest -m "not slow"
```

### Full Test Suite
```bash
# All tests
pytest

# All tests with detailed coverage
pytest --cov=ctx --cov-report=html
```

### Specific Test Categories
```bash
# Only regression tests for bugs we fixed
pytest -k "regression"

# Only CLI-related tests
pytest tests/integration/test_cli_integration.py

# Only MCP-related tests  
pytest -m mcp

# Only multimodal sync tests
pytest tests/multimodal/
```

## Test Fixtures

### Core Fixtures (from `conftest.py`)

- `temp_storage_dir`: Temporary directory for test storage
- `ctx_manager`: Clean ContextManager instance
- `sample_context`: Pre-configured test context
- `populated_manager`: Manager with test data
- `cli_runner`: Click CLI test runner
- `mcp_test_client`: MCP server test client
- `multimodal_test_env`: Complete testing environment

### Usage Example

```python
def test_context_creation(ctx_manager):
    """Test using the ctx_manager fixture"""
    context = ctx_manager.create("test", "Test context")
    assert context.name == "test"

def test_multimodal_sync(multimodal_test_env):
    """Test using the multimodal environment"""
    env = multimodal_test_env
    context = env.create_test_context("sync-test")
    # Test CLI-MCP synchronization
    sync_data = env.verify_sync("sync-test")
    assert sync_data["api_context"] is not None
```

## Regression Tests

We maintain specific regression tests for critical bugs we've fixed:

### CLI Notes Command Fix
**Issue**: Click namespace collision causing `TypeError: object of type 'Note' has no len()`  
**Fix**: Used slicing instead of `reversed()` function  
**Test**: `test_notes_command_no_recursion_bug`

### MCP Server Initialization
**Issue**: Missing `initialize` method causing "No tools or prompts" error  
**Fix**: Added proper MCP protocol initialization sequence  
**Test**: `test_mcp_initialization_fix`

### Multimodal Synchronization  
**Issue**: CLI and MCP showing inconsistent data  
**Fix**: Fixed storage path handling and protocol implementation  
**Test**: `test_state_change_sync`, `test_bidirectional_state_sync`

## Coverage Requirements

- **Unit Tests**: >= 90% coverage for `ctx/` modules
- **Integration Tests**: All CLI commands must have tests
- **Multimodal Tests**: All MCP tools must have sync tests
- **Overall**: >= 80% total coverage

## Performance Guidelines

- **Unit tests**: < 1 second each
- **Integration tests**: < 5 seconds each  
- **MCP tests**: < 10 seconds each
- **Multimodal tests**: < 15 seconds each
- **Full suite**: < 2 minutes total

## Continuous Integration

### Pre-merge Requirements
```bash
# Required checks
pytest -m "unit or integration" --cov=ctx --cov-fail-under=80
pytest -m "not slow"  # Quick smoke tests
```

### Nightly/Release Testing
```bash
# Full comprehensive testing
pytest --cov=ctx --cov-report=html --cov-fail-under=85
pytest -m slow  # All tests including slow ones
```

## Writing New Tests

### Test Naming Convention
- Files: `test_<module_name>.py`
- Classes: `Test<FeatureName>`  
- Functions: `test_<specific_behavior>`

### Test Structure
```python
def test_specific_behavior(fixture):
    """Test description explaining what behavior is verified"""
    # Arrange
    setup_data = create_test_data()
    
    # Act  
    result = perform_operation(setup_data)
    
    # Assert
    assert result.expected_property == expected_value
    assert len(result.items) == expected_count
```

### Adding Regression Tests
When fixing a bug:

1. Create a test that reproduces the bug
2. Verify the test fails with the current code
3. Fix the bug
4. Verify the test passes
5. Add to appropriate regression test class

## Debugging Tests

### Run Single Test
```bash
pytest tests/unit/test_models.py::TestContext::test_add_note -v
```

### Debug Mode
```bash
pytest --pdb  # Drop into debugger on failure
pytest -s     # Show print statements
```

### Coverage Analysis
```bash
pytest --cov=ctx --cov-report=html
# Open htmlcov/index.html to see detailed coverage
```

## Test Data Management

- Use fixtures for consistent test data
- Isolate tests with temporary directories
- Clean up resources after tests
- Mock external dependencies appropriately

## Best Practices

1. **Test Independence**: Each test should run independently
2. **Clear Assertions**: Use descriptive assertion messages
3. **Edge Cases**: Test boundary conditions and error cases
4. **Documentation**: Include docstrings explaining test purpose
5. **Maintainability**: Keep tests simple and focused

## Troubleshooting Common Issues

### MCP Tests Skipping
If MCP tests are being skipped:
- Ensure `cursor_ctx_integration.py` is executable
- Check that `ctx` command is in PATH
- Verify Python environment has required dependencies

### CLI Tests Failing
If CLI tests are failing:
- Check that `ctx` package is installed in development mode
- Verify test isolation with temporary directories
- Ensure environment variables are properly set/cleaned

### Multimodal Tests Inconsistent
If multimodal sync tests are flaky:
- Add small delays between operations
- Verify storage path isolation
- Check for race conditions in async operations

This comprehensive testing strategy ensures the reliability and robustness of the ctx-tools multimodal integration while preventing regressions and maintaining code quality.