"""Tests for due date support in tasks.py — domain-agent lane. Written before implementation."""
import pytest
from task_cli import tasks


def test_add_task_without_due_date_has_none():
    task_list = []
    task = tasks.add(task_list, "Buy milk")
    assert task.get("due_date") is None


def test_add_task_with_valid_due_date():
    task_list = []
    task = tasks.add(task_list, "File taxes", due_date="2026-04-20")
    assert task["due_date"] == "2026-04-20"


def test_add_task_with_invalid_due_date_raises():
    task_list = []
    with pytest.raises(ValueError):
        tasks.add(task_list, "Bad task", due_date="not-a-date")


def test_add_task_with_wrong_format_raises():
    task_list = []
    with pytest.raises(ValueError):
        tasks.add(task_list, "Wrong format", due_date="20-04-2026")


def test_due_date_stored_in_task_dict():
    task_list = []
    task = tasks.add(task_list, "Reminder", due_date="2026-12-31")
    assert task_list[0]["due_date"] == "2026-12-31"
