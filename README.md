# task-cli

A minimal command-line task tracker. Tasks are stored in a local JSON file.

## Usage

```bash
python -m task_cli add "Buy milk"      # add a task
python -m task_cli list                 # list all tasks
python -m task_cli done <id>            # mark a task done
python -m task_cli delete <id>          # delete a task
```

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install pytest pytest-cov
```

## Testing

```bash
pytest
pytest --cov=src --cov-report=term-missing
```

## Storage

Tasks are saved to `~/.task-cli/tasks.json` by default.  
Override with the `TASK_CLI_FILE` environment variable:

```bash
TASK_CLI_FILE=/tmp/my-tasks.json python -m task_cli list
```
