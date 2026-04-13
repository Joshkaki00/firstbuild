# CLAUDE.md

## Project

**task-cli** — a command-line task tracker. Users add, list, complete, and delete tasks stored in a local JSON file.

## Tech Stack

- **Language**: Python 3.11+
- **Testing**: `pytest` with `pytest-cov`
- **No external runtime dependencies** — stdlib only (`json`, `argparse`, `pathlib`)

## Structure

```
src/task_cli/      # application code
  __init__.py
  cli.py           # argparse entry point
  store.py         # JSON read/write logic
  tasks.py         # task domain logic
tests/             # pytest test files, mirror src structure
```

## Commands

```bash
python -m task_cli add "Buy milk"
python -m task_cli list
python -m task_cli done <id>
python -m task_cli delete <id>
```

## Testing

```bash
pytest                        # run all tests
pytest --cov=src --cov-report=term-missing   # with coverage
```

- Write the failing test first. Commit it. Then implement.
- Each feature must have tests before any implementation lands.
- Keep tests isolated — use `tmp_path` fixtures, never touch real files.
- Target: 90%+ line coverage on `src/`.

## Conventions

- Functions over classes where possible.
- `store.py` owns all file I/O. `tasks.py` owns domain logic. `cli.py` wires them.
- See `src/task_cli/store.py` for the JSON schema used for tasks.
- Errors surface as printed messages + non-zero exit codes, not exceptions.

## Quality Gates

See `spec.md`.
