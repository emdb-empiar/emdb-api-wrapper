# EMDB API Wrapper Tests

This directory contains the unit tests for the EMDB API Wrapper project.

## Test Structure

- **test_exceptions.py** - Tests for all exception classes in `emdb/exceptions.py`
- **test_utils.py** - Tests for utility functions in `emdb/utils.py`, including rate limiting and HTTP request handling
- **test_client.py** - Tests for the main EMDB client class in `emdb/client.py`
- **test_search.py** - Tests for search functionality and lazy entry loading in `emdb/models/search.py` and `emdb/models/lazy_entry.py`

## Running Tests

### Run all tests
```bash
pytest
```

### Run with verbose output
```bash
pytest -v
```

### Run specific test file
```bash
pytest tests/test_client.py
```

### Run specific test class
```bash
pytest tests/test_client.py::TestEMDBClient
```

### Run specific test function
```bash
pytest tests/test_client.py::TestEMDBClient::test_get_entry_success
```

### Run with coverage report
```bash
pytest --cov=emdb --cov-report=html
```

This will generate a coverage report in `htmlcov/index.html`.

### Run with coverage report in terminal
```bash
pytest --cov=emdb --cov-report=term-missing
```

## Test Dependencies

The tests use the following libraries:
- **pytest** - Testing framework
- **pytest-mock** - Mocking support for pytest
- **pytest-cov** - Coverage reporting
- **responses** - HTTP request mocking

Install test dependencies:
```bash
pip install -e ".[test]"
```

## Writing New Tests

When adding new tests:

1. Follow the existing naming conventions (`test_*.py`)
2. Group related tests into classes (e.g., `TestEMDBClient`)
3. Use descriptive test names that explain what is being tested
4. Include docstrings explaining the purpose of each test
5. Use appropriate mocking for external dependencies (HTTP requests, file I/O)
6. Test both success cases and error conditions
7. Keep tests focused and independent

## Current Coverage

As of the latest test run, the test suite achieves approximately **52% code coverage** with **45 passing tests**.

Key areas covered:
- ✅ Exception handling (100% coverage)
- ✅ Utility functions (100% coverage)
- ✅ Client API methods (89% coverage)
- ✅ Search and lazy loading (96% coverage)
- ⚠️ Models (partial coverage - annotations, entry, validation, plots, files)

Future test additions should focus on:
- Model classes (`emdb/models/entry.py`, `emdb/models/validation.py`, etc.)
- File download functionality
- Plot generation
- Annotation parsing
