# spec.md — task-cli Specification

## Overview

`task-cli` is a command-line tool for managing tasks stored in a local JSON file (`~/.task-cli/tasks.json` by default, overridable via `TASK_CLI_FILE` env var).

---

## Quality Gates

### QG-1: Add and List Tasks

**Invoke:**
```bash
python -m task_cli add "Write tests"
python -m task_cli list
```

**Success criteria:**
- Exit code 0 for both commands.
- `add` prints a confirmation with the new task's ID.
- `list` displays the task with its ID, status (`todo`), and description.

---

### QG-2: Complete a Task

**Invoke:**
```bash
python -m task_cli add "Write tests"
python -m task_cli done 1
python -m task_cli list
```

**Success criteria:**
- Exit code 0 for all commands.
- After `done 1`, `list` shows the task with status `done`.
- Running `done <nonexistent-id>` exits with code 1 and prints an error.

---

### QG-3: Delete a Task

**Invoke:**
```bash
python -m task_cli add "Temporary task"
python -m task_cli delete 1
python -m task_cli list
```

**Success criteria:**
- Exit code 0 for all commands.
- After `delete 1`, `list` no longer shows the task.
- Running `delete <nonexistent-id>` exits with code 1 and prints an error.

---

## Acceptance Criteria

### AC-1: Add a task
- **Given** the CLI is installed and no tasks exist
- **When** I run `python -m task_cli add "Buy milk"`
- **Then** the task is saved with a unique integer ID, status `todo`, and the description "Buy milk"; exit code is 0

### AC-2: List tasks shows all items
- **Given** two tasks have been added
- **When** I run `python -m task_cli list`
- **Then** both tasks appear with their IDs, statuses, and descriptions; exit code is 0

### AC-3: Marking a task done changes its status
- **Given** a task with ID 1 exists and has status `todo`
- **When** I run `python -m task_cli done 1`
- **Then** the task's status changes to `done` and `list` reflects the update; exit code is 0

### AC-4: Deleting a task removes it permanently
- **Given** a task with ID 2 exists
- **When** I run `python -m task_cli delete 2`
- **Then** the task is no longer present in `list` output; exit code is 0

### AC-5: Invalid ID produces a clear error
- **Given** no task with ID 999 exists
- **When** I run `python -m task_cli done 999` or `python -m task_cli delete 999`
- **Then** an error message is printed to stderr and the exit code is 1
