# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a newly initialized Python repository ("Claude-run") with no source code yet. The `.gitignore` is configured for Python projects and covers common tooling: pytest, coverage, mypy, ruff, Django, Flask, Streamlit, Marimo, Jupyter, and several package managers (pip, poetry, uv, pdm, pixi).

## Project Setup

No build system, test runner, or dependency manager has been configured yet. When adding code, choose tooling appropriate to the project type and document the commands here.

**Recommended starting points (update when established):**
- Package manager: `uv`, `poetry`, or `pip` + `requirements.txt`
- Linter/formatter: `ruff` (already in `.gitignore`)
- Type checker: `mypy` (already in `.gitignore`)
- Test runner: `pytest` (already in `.gitignore`)

Once tooling is chosen, replace this section with the actual commands:
```
# Example — fill in once established
uv run pytest                        # run all tests
uv run pytest tests/test_foo.py      # run a single test file
uv run ruff check .                  # lint
uv run mypy .                        # type-check
```

## Development Branch

Active development happens on feature branches; `main` is the stable branch. The current working branch is `claude/add-claude-documentation-PRxkq`.
