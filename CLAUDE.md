# Omegapoint Codebase Guidelines

## Commands
- Install: `pip install -e .`
- Install dev dependencies: `pip install -e ".[dev]"`
- Run all tests: `pytest`
- Run specific test: `pytest tests/test_utils.py::test_weekdays`
- Run tests with coverage: `pytest --cov=omegapoint`
- Check types: `mypy omegapoint`

## Code Style Guidelines

### Imports
- Group standard library imports first, followed by third-party packages, then local imports
- Use absolute imports from the package (e.g., `from omegapoint import schema, utils`)
- Use explicit imports rather than wildcard imports

### Formatting
- Follow PEP 8 with 4-space indentation
- Line length appears to be ~88 characters
- Use single quotes for strings unless double quotes are needed

### Types
- Use type hints for all new code
- For variable annotations, prefer `name: type = value` format
- For function annotations, include return type: `def func(arg: type) -> return_type:`
- Use types from the typing module for complex types (List, Dict, Optional, etc.)

### Naming Conventions
- snake_case for functions and variables
- CamelCase for classes
- Constants in UPPER_CASE
- Descriptive names that indicate purpose or function

### Error Handling
- Use custom GqlError for GraphQL-related exceptions
- Use validation functions from validation.py for input validation
- Return error collections when dealing with batch operations
- Use descriptive error messages
- Always catch exceptions at appropriate levels

### Documentation
- Use docstrings for all modules, classes, and functions
- Follow Google style docstrings with Args, Returns, Raises sections
- Include examples in docstrings for non-trivial functions
- Important notes about API parameters should be in docstrings
- Add type info in docstrings if not using type annotations

### Libraries
- Core dependencies: numpy, pandas, requests, sgqlc
- Dev dependencies: pytest, pytest-cov, mypy, twine

### Testing
- Write tests for all new functionality
- Organize tests to mirror the package structure
- Use pytest fixtures for common test data
- Mock external dependencies using unittest.mock