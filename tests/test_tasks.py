"""Tests for tasks.py — domain logic. Written before implementation."""
import pytest
from task_cli import tasks


def test_add_task_returns_task_with_id():
    task_list = []
    task = tasks.add(task_list, "Buy milk")
    assert task["id"] == 1
    assert task["description"] == "Buy milk"
    assert task["status"] == "todo"


def test_add_task_appends_to_list():
    task_list = []
    tasks.add(task_list, "First")
    tasks.add(task_list, "Second")
    assert len(task_list) == 2


def test_add_task_ids_are_sequential():
    task_list = []
    t1 = tasks.add(task_list, "First")
    t2 = tasks.add(task_list, "Second")
    assert t2["id"] == t1["id"] + 1


def test_add_task_ids_skip_deleted_gaps():
    task_list = [{"id": 3, "description": "Old", "status": "done"}]
    new = tasks.add(task_list, "New")
    assert new["id"] == 4


def test_mark_done_changes_status():
    task_list = [{"id": 1, "description": "Buy milk", "status": "todo"}]
    tasks.mark_done(task_list, 1)
    assert task_list[0]["status"] == "done"


def test_mark_done_raises_for_missing_id():
    task_list = []
    with pytest.raises(KeyError):
        tasks.mark_done(task_list, 999)


def test_delete_removes_task():
    task_list = [
        {"id": 1, "description": "Keep", "status": "todo"},
        {"id": 2, "description": "Remove", "status": "todo"},
    ]
    tasks.delete(task_list, 2)
    assert len(task_list) == 1
    assert task_list[0]["id"] == 1


def test_delete_raises_for_missing_id():
    task_list = []
    with pytest.raises(KeyError):
        tasks.delete(task_list, 999)


def test_list_all_returns_all_tasks():
    task_list = [
        {"id": 1, "description": "A", "status": "todo"},
        {"id": 2, "description": "B", "status": "done"},
    ]
    result = tasks.list_all(task_list)
    assert result == task_list
