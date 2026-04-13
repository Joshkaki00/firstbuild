"""Tests verifying store persists due_date field — store-agent lane."""
from task_cli import store


def test_due_date_field_survives_roundtrip(tmp_path):
    path = tmp_path / "tasks.json"
    tasks = [{"id": 1, "description": "File taxes", "status": "todo", "priority": "medium", "due_date": "2026-04-20"}]
    store.save(path, tasks)
    loaded = store.load(path)
    assert loaded[0]["due_date"] == "2026-04-20"


def test_due_date_none_survives_roundtrip(tmp_path):
    path = tmp_path / "tasks.json"
    tasks = [{"id": 1, "description": "Buy milk", "status": "todo", "priority": "medium", "due_date": None}]
    store.save(path, tasks)
    loaded = store.load(path)
    assert loaded[0]["due_date"] is None
