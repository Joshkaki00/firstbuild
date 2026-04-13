# /tdd — Scaffold a red/green/refactor cycle for a new feature

Use this when adding a new feature. Follow these steps in order — do not skip ahead.

## Arguments

The user will provide a feature description, e.g.: `/tdd add due dates to tasks`

## Steps

### 1. Red — write failing tests first

- Identify which modules the feature touches (see `CLAUDE.md` for architecture).
- Write tests in the appropriate `tests/test_<module>_<feature>.py` file.
- Run the tests and confirm they fail before writing any implementation.
- Commit the failing tests:
  ```
  git add tests/ && git commit -m "test(<module>/<feature>): failing tests for <feature>"
  ```

### 2. Green — implement until tests pass

- Implement only what is needed to make the tests pass. No more.
- Run the full suite (`/test`) to confirm nothing regressed.
- Commit the implementation:
  ```
  git add src/ && git commit -m "feat(<module>/<feature>): implement <feature>"
  ```

### 3. Refactor — clean up while keeping tests green

- Look for duplication, unclear names, or violations of the architecture in `CLAUDE.md`.
- Run `/test` after every change to stay green.
- Commit if any refactoring was done:
  ```
  git commit -m "refactor(<module>): <what and why>"
  ```

## Rules

- Never commit implementation before the failing test commit.
- Keep tests isolated — use `tmp_path` and `TASK_CLI_FILE`, never touch real files.
- Each layer owns its concern: `store.py` = I/O, `tasks.py` = logic, `cli.py` = wiring.
