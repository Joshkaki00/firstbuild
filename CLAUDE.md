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
python -m task_cli add "File taxes" --due 2026-04-20  # optional due date, YYYY-MM-DD
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
PYTHONPATH=src pytest                                              # run all tests
PYTHONPATH=src pytest tests/test_cli.py                            # run a single test file
PYTHONPATH=src pytest tests/test_cli.py::test_add_task             # run a single test
PYTHONPATH=src pytest --cov=src --cov-report=term-missing          # with coverage
```

Custom slash commands are available for the common workflows:

- `/test` — run the full suite with coverage and report pass/fail
- `/tdd <feature>` — scaffold a red/green/refactor cycle for a new feature
- `/qg` — run all three quality gates from `spec.md` against a temp file
- `/verify` — full 4-step pipeline: import check → syntax check → tests → coverage gate

- Write the failing test first. Commit it. Then implement.
- Each feature must have tests before any implementation lands.
- Keep tests isolated — use `tmp_path` fixtures and `TASK_CLI_FILE` env var, never touch real files.
- Coverage note: `cli.py` and `__main__.py` show 0% in `--cov` reports because CLI tests run via subprocess. `store.py` and `tasks.py` should stay at 100%.
- New features get companion test files per layer (e.g., `test_tasks_priority.py`, `test_store_priority.py`, `test_cli_priority.py`), not additions to the core test files.

## Architecture

`store.py` owns all file I/O. `tasks.py` owns domain logic. `cli.py` wires them together — it loads from store, calls tasks functions, saves back to store, then prints results and returns an exit code.

Each `cmd_*` function in `cli.py` follows the same pattern: load → mutate → save → print → return exit code. Errors from `tasks.py` (`ValueError`, `KeyError`) are caught here, printed to stderr, and converted to exit code 1.

### JSON task schema

```json
{"id": 1, "description": "Buy milk", "status": "todo", "priority": "medium", "due_date": "2026-04-20"}
```

- `status`: `"todo"` or `"done"`
- `priority`: `"high"`, `"medium"`, or `"low"` (validated in `tasks.py` against `VALID_PRIORITIES`)
- `due_date`: ISO 8601 string (`"YYYY-MM-DD"`) or `null`; validated via `datetime.date.fromisoformat` in `tasks.py`
- IDs are auto-incremented integers (`max existing id + 1`); deleted IDs are never reused
- `priority` was added after initial release — `cmd_list` uses `.get('priority', 'medium')` to handle older tasks that lack the field

## Conventions

- Functions over classes where possible.
- Errors surface as printed messages + non-zero exit codes, not exceptions.
- New optional task fields must use `.get('field', default)` in `cmd_list` to stay backward-compatible with tasks written before the field existed (see `priority` and `due_date` as precedents).

## Hallucination Patterns (Gotcha Log)

Patterns observed during this build where AI output needed verification or correction:

- **Wrong build backend path.** Agent used `setuptools.backends.legacy:build` in `pyproject.toml`. Correct value is `setuptools.build_meta`. Always verify `[build-system]` entries against the current setuptools docs before running `pip install -e .`.
- **`<placeholder>` syntax in shell examples.** Agent wrote `done <id>` and `delete <id>` in README and CLAUDE.md. Angle brackets are shell redirect operators — zsh/bash interpret `<id>` as "read stdin from a file named id." Always use a real example value (e.g., `done 1`) in any runnable code block.
- **Subprocess coverage gap not anticipated.** Agent wrote CLI tests using `subprocess.run` without flagging that pytest-cov won't instrument child processes. This causes `cli.py` and `__main__.py` to report 0% coverage despite being fully tested. If coverage completeness matters, prefer calling `cli.main()` directly in tests instead of spawning subprocesses.
- **Unused import not caught.** `test_cli.py` imported `pytest` without using it. Linter would catch this; agent did not flag it during generation.

## Quality Gates

See `spec.md` for the 3 quality gates and 5 acceptance criteria.
