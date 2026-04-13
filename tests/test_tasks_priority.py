"""Tests for priority support in tasks.py — domain-agent lane. Written before implementation."""
import pytest
from task_cli import tasks


def test_add_task_default_priority_is_medium():
    task_list = []
    task = tasks.add(task_list, "Buy milk")
    assert task["priority"] == "medium"


def test_add_task_accepts_high_priority():
    task_list = []
    task = tasks.add(task_list, "Urgent thing", priority="high")
    assert task["priority"] == "high"


def test_add_task_accepts_low_priority():
    task_list = []
    task = tasks.add(task_list, "Someday thing", priority="low")
    assert task["priority"] == "low"


def test_add_task_rejects_invalid_priority():
    task_list = []
    with pytest.raises(ValueError):
        tasks.add(task_list, "Bad task", priority="critical")


def test_list_by_priority_filters_correctly():
    task_list = []
    tasks.add(task_list, "High thing", priority="high")
    tasks.add(task_list, "Low thing", priority="low")
    tasks.add(task_list, "Medium thing", priority="medium")
    result = tasks.list_by_priority(task_list, "high")
    assert len(result) == 1
    assert result[0]["description"] == "High thing"


def test_list_by_priority_returns_all_when_none_given():
    task_list = []
    tasks.add(task_list, "A", priority="high")
    tasks.add(task_list, "B", priority="low")
    result = tasks.list_by_priority(task_list, None)
    assert len(result) == 2


def test_list_by_priority_invalid_filter_raises():
    task_list = []
    with pytest.raises(ValueError):
        tasks.list_by_priority(task_list, "urgent")
