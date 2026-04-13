"""Argparse entry point. Wires CLI commands to tasks and store."""
import argparse
import os
import sys
from pathlib import Path

from task_cli import store, tasks

DEFAULT_FILE = Path.home() / ".task-cli" / "tasks.json"


def _task_file() -> Path:
    return Path(os.environ.get("TASK_CLI_FILE", DEFAULT_FILE))


def cmd_add(args: argparse.Namespace) -> int:
    path = _task_file()
    task_list = store.load(path)
    try:
        task = tasks.add(task_list, args.description, priority=args.priority)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    store.save(path, task_list)
    print(f"Added task #{task['id']} [{task['priority']}]: {task['description']}")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    path = _task_file()
    task_list = store.load(path)
    try:
        visible = tasks.list_by_priority(task_list, args.priority)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    if not visible:
        print("No tasks yet. Use 'add' to create one.")
        return 0
    for task in visible:
        print(f"[{task['status']}] #{task['id']}  ({task.get('priority', 'medium')})  {task['description']}")
    return 0


def cmd_done(args: argparse.Namespace) -> int:
    path = _task_file()
    task_list = store.load(path)
    try:
        tasks.mark_done(task_list, args.id)
    except KeyError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    store.save(path, task_list)
    print(f"Marked #{args.id} as done.")
    return 0


def cmd_delete(args: argparse.Namespace) -> int:
    path = _task_file()
    task_list = store.load(path)
    try:
        tasks.delete(task_list, args.id)
    except KeyError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    store.save(path, task_list)
    print(f"Deleted task #{args.id}.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="task-cli", description="Minimal task tracker")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="Add a new task")
    p_add.add_argument("description", help="Task description")
    p_add.add_argument("--priority", default="medium", choices=["high", "medium", "low"], help="Task priority")
    p_add.set_defaults(func=cmd_add)

    p_list = sub.add_parser("list", help="List all tasks")
    p_list.add_argument("--priority", default=None, choices=["high", "medium", "low"], help="Filter by priority")
    p_list.set_defaults(func=cmd_list)

    p_done = sub.add_parser("done", help="Mark a task as done")
    p_done.add_argument("id", type=int, help="Task ID")
    p_done.set_defaults(func=cmd_done)

    p_del = sub.add_parser("delete", help="Delete a task")
    p_del.add_argument("id", type=int, help="Task ID")
    p_del.set_defaults(func=cmd_delete)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)
