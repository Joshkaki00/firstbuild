"""Domain logic for task operations. No file I/O here."""


def _next_id(task_list: list[dict]) -> int:
    if not task_list:
        return 1
    return max(t["id"] for t in task_list) + 1


def add(task_list: list[dict], description: str) -> dict:
    task = {"id": _next_id(task_list), "description": description, "status": "todo"}
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
