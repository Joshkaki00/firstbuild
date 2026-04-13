"""Domain logic for task operations. No file I/O here."""
from datetime import date

VALID_PRIORITIES = {"high", "medium", "low"}


def _next_id(task_list: list[dict]) -> int:
    if not task_list:
        return 1
    return max(t["id"] for t in task_list) + 1


def _validate_due_date(due_date: str | None) -> None:
    if due_date is None:
        return
    try:
        date.fromisoformat(due_date)
    except ValueError:
        raise ValueError(f"Invalid due date '{due_date}'. Use YYYY-MM-DD format.")


def add(task_list: list[dict], description: str, priority: str = "medium", due_date: str | None = None) -> dict:
    if priority not in VALID_PRIORITIES:
        raise ValueError(f"Invalid priority '{priority}'. Choose from: {', '.join(sorted(VALID_PRIORITIES))}")
    _validate_due_date(due_date)
    task = {"id": _next_id(task_list), "description": description, "status": "todo", "priority": priority, "due_date": due_date}
    task_list.append(task)
    return task


def mark_done(task_list: list[dict], task_id: int) -> None:
    for task in task_list:
        if task["id"] == task_id:
            task["status"] = "done"
            return
    raise KeyError(f"No task with id {task_id}")


def delete(task_list: list[dict], task_id: int) -> None:
    for i, task in enumerate(task_list):
        if task["id"] == task_id:
            task_list.pop(i)
            return
    raise KeyError(f"No task with id {task_id}")


def list_all(task_list: list[dict]) -> list[dict]:
    return task_list


def list_by_priority(task_list: list[dict], priority: str | None) -> list[dict]:
    if priority is None:
        return task_list
    if priority not in VALID_PRIORITIES:
        raise ValueError(f"Invalid priority '{priority}'. Choose from: {', '.join(sorted(VALID_PRIORITIES))}")
    return [t for t in task_list if t.get("priority") == priority]
