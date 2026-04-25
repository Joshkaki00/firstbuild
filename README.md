# task-cli

A minimal command-line task tracker built as part of the [Claude Code in Action](https://www.anthropic.com) course on Skilljar. Tasks are stored in a local JSON file.

## Usage

```bash
python -m task_cli add "Buy milk"                         # add a task (default priority: medium)
python -m task_cli add "Urgent thing" --priority high     # priority: high, medium, or low
python -m task_cli add "File taxes" --due 2026-04-20      # optional due date (YYYY-MM-DD)
python -m task_cli list                                   # list all tasks
python -m task_cli list --priority high                   # filter by priority
python -m task_cli done 1                                 # mark task #1 as done
python -m task_cli delete 1                               # delete task #1
```

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e .
pip install pytest pytest-cov
```

## Testing

```bash
pytest                                        # run all tests (63 total)
pytest --cov=src --cov-report=term-missing    # with coverage
```

> **Note:** `cli.py` shows 0% coverage in reports because CLI tests run via subprocess. `store.py` and `tasks.py` stay at 100%.

## Storage

Tasks are saved to `~/.task-cli/tasks.json` by default.  
Override with the `TASK_CLI_FILE` environment variable:

```bash
TASK_CLI_FILE=/tmp/my-tasks.json python -m task_cli list
```

## Task Schema

```json
{"id": 1, "description": "Buy milk", "status": "todo", "priority": "medium", "due_date": null}
```

## Development

This project was built with a test-first workflow using Claude Code. Key dev files:

- `CLAUDE.md` — agent context: tech stack, architecture, conventions, gotcha log
- `spec.md` — quality gates and acceptance criteria mapped to tests
- `workflow-audit.md` — course audit, feature inventory, and new technique documentation
- `.claude/commands/` — custom slash commands: `/test`, `/tdd`, `/qg`, `/verify`, `/scaffold`
- `.claude/settings.json` — PostToolUse hook: syntax check after every file edit
- `.mcp.json` — Context7 MCP for live documentation verification

## Completion

Quiz: 8/8 correct (100%) on the Claude Code in Action final quiz.

![Quiz score — 8 of 8 correct (100%)](images/Screenshot%202026-04-24%20at%2015-01-19%20Quiz%20on%20Claude%20Code.png)

![Completion email from Anthropic Education](images/Gmail%20-%20Completion%20of%20Claude%20Code%20in%20Action.jpg)
