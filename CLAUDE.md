# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

**task-cli** — a command-line task tracker. Users add, list, complete, and delete tasks stored in a local JSON file (`~/.task-cli/tasks.json` by default, overridable via `TASK_CLI_FILE` env var).

## Tech Stack

- **Language**: Python 3.11+
- **Testing**: `pytest` with `pytest-cov`
- **No external runtime dependencies** — stdlib only (`json`, `argparse`, `pathlib`)

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e .
pip install pytest pytest-cov
```

## Commands

```bash
python -m task_cli add "Buy milk"
python -m task_cli add "Buy milk" --priority high   # priorities: high, medium (default), low
python -m task_cli list
python -m task_cli list --priority high             # filter by priority
python -m task_cli done 1
python -m task_cli delete 1
```

Override the storage file (useful during development):

```bash
TASK_CLI_FILE=/tmp/my-tasks.json python -m task_cli list
```

## Testing

```bash
pytest                                              # run all tests
pytest tests/test_cli.py                            # run a single test file
pytest tests/test_cli.py::test_add_task             # run a single test
pytest --cov=src --cov-report=term-missing          # with coverage
```

- Write the failing test first. Commit it. Then implement.
- Each feature must have tests before any implementation lands.
- Keep tests isolated — use `tmp_path` fixtures and `TASK_CLI_FILE` env var, never touch real files.
- Coverage note: `cli.py` and `__main__.py` show 0% in `--cov` reports because CLI tests run via subprocess. `store.py` and `tasks.py` should stay at 100%.

## Architecture

`store.py` owns all file I/O. `tasks.py` owns domain logic. `cli.py` wires them together — it loads from store, calls tasks functions, saves back to store, then prints results and returns an exit code.

Each `cmd_*` function in `cli.py` follows the same pattern: load → mutate → save → print → return exit code. Errors from `tasks.py` (`ValueError`, `KeyError`) are caught here, printed to stderr, and converted to exit code 1.

### JSON task schema

```json
{"id": 1, "description": "Buy milk", "status": "todo", "priority": "medium"}
```

- `status`: `"todo"` or `"done"`
- `priority`: `"high"`, `"medium"`, or `"low"` (validated in `tasks.py` against `VALID_PRIORITIES`)
- IDs are auto-incremented integers (`max existing id + 1`)

## Conventions

- Functions over classes where possible.
- Errors surface as printed messages + non-zero exit codes, not exceptions.

## Quality Gates

See `spec.md` for the 3 quality gates and 5 acceptance criteria.
