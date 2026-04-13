"""Tests verifying store persists priority field — store-agent lane."""
from task_cli import store


def test_priority_field_survives_roundtrip(tmp_path):
    path = tmp_path / "tasks.json"
    tasks = [{"id": 1, "description": "Urgent", "status": "todo", "priority": "high"}]
    store.save(path, tasks)
    loaded = store.load(path)
    assert loaded[0]["priority"] == "high"


def test_multiple_priorities_roundtrip(tmp_path):
    path = tmp_path / "tasks.json"
    tasks = [
        {"id": 1, "description": "A", "status": "todo", "priority": "high"},
        {"id": 2, "description": "B", "status": "todo", "priority": "low"},
        {"id": 3, "description": "C", "status": "done", "priority": "medium"},
    ]
    store.save(path, tasks)
    loaded = store.load(path)
    priorities = [t["priority"] for t in loaded]
    assert priorities == ["high", "low", "medium"]
