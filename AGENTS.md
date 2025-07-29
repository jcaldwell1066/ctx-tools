# CTX Project Agent Guidelines

This file contains instructions for all AI agents working on the `ctx-tools` repository.

## Development Workflow

1. Install development dependencies before running tests:

   ```bash
   pip install -e ".[dev]"
   ```

2. Run the test suite with **pytest** before committing changes:

   ```bash
   pytest
   ```

   You can run specific test groups using markers defined in [`docs/TESTING.md`](docs/TESTING.md):

   ```bash
   pytest -m unit         # Unit tests only
   pytest -m integration  # Integration tests
   pytest -m mcp          # MCP integration tests
   ```

3. Format Python code with **black** and perform type checking with **mypy**:

   ```bash
   black ctx/
   mypy ctx/
   ```

   These commands are also referenced in the [README](README.md) for human developers.

## Commit Standards

- Write clear, concise commit messages that describe the change.
- Include tests for new functionality whenever possible.
- Ensure the codebase remains type annotated and well documented.

## Pull Requests

When opening a pull request, provide a brief summary of the changes and reference any relevant documentation in the `docs/` folder.

