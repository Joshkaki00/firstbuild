"""Edge case tests for tasks.py — gaps identified by test gap analysis.

These cover boundary conditions and failure modes that the happy-path tests miss,
per the 'Nothing Survives First Contact' verification checklist.
"""
import pytest
from task_cli import tasks


def test_add_empty_description_is_allowed():
    """Empty string is technically valid — CLI owns the UX decision, not domain."""
    task_list = []
    task = tasks.add(task_list, "")
    assert task["description"] == ""
    assert task["id"] == 1


def test_add_very_long_description():
    task_list = []
    long_desc = "x" * 10_000
    task = tasks.add(task_list, long_desc)
    assert task["description"] == long_desc


def test_add_description_with_special_characters():
    task_list = []
    task = tasks.add(task_list, 'Buy "milk" & eggs — café ☕')
    assert task["description"] == 'Buy "milk" & eggs — café ☕'


def test_add_description_with_newlines():
    task_list = []
    task = tasks.add(task_list, "line one\nline two")
    assert task["description"] == "line one\nline two"


def test_mark_done_on_already_done_task():
    """Marking done twice is idempotent — should not raise."""
    task_list = [{"id": 1, "description": "A", "status": "done"}]
    tasks.mark_done(task_list, 1)
    assert task_list[0]["status"] == "done"


def test_delete_from_single_item_list_leaves_empty():
    task_list = [{"id": 1, "description": "Only one", "status": "todo"}]
    tasks.delete(task_list, 1)
    assert task_list == []


def test_add_many_tasks_ids_are_unique():
    task_list = []
    for i in range(100):
        tasks.add(task_list, f"Task {i}")
    ids = [t["id"] for t in task_list]
    assert len(ids) == len(set(ids))


def test_id_continues_after_delete():
    """ID assignment uses max+1, so gaps after delete don't reset the counter."""
    task_list = []
    tasks.add(task_list, "First")   # id=1
    tasks.add(task_list, "Second")  # id=2
    tasks.delete(task_list, 1)
    new = tasks.add(task_list, "Third")
    assert new["id"] == 3  # not 1, not 2


def test_list_by_priority_on_empty_list():
    assert tasks.list_by_priority([], "high") == []


def test_list_by_priority_with_tasks_missing_priority_field():
    """Old tasks (pre-priority feature) lack the field — should not crash."""
    task_list = [{"id": 1, "description": "Old task", "status": "todo"}]
    result = tasks.list_by_priority(task_list, "high")
    assert result == []
