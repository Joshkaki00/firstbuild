"""Tests for store.py — JSON read/write layer. Written before implementation."""
import json
import pytest
from task_cli import store


def test_load_returns_empty_list_when_file_missing(tmp_path):
    path = tmp_path / "tasks.json"
    result = store.load(path)
    assert result == []


def test_save_creates_file_with_tasks(tmp_path):
    path = tmp_path / "tasks.json"
    tasks = [{"id": 1, "description": "Buy milk", "status": "todo"}]
    store.save(path, tasks)
    assert path.exists()


def test_save_and_load_roundtrip(tmp_path):
    path = tmp_path / "tasks.json"
    tasks = [
        {"id": 1, "description": "Buy milk", "status": "todo"},
        {"id": 2, "description": "Write tests", "status": "done"},
    ]
    store.save(path, tasks)
    result = store.load(path)
    assert result == tasks


def test_save_writes_valid_json(tmp_path):
    path = tmp_path / "tasks.json"
    tasks = [{"id": 1, "description": "Test", "status": "todo"}]
    store.save(path, tasks)
    raw = json.loads(path.read_text())
    assert raw == tasks


def test_load_creates_parent_dirs_on_save(tmp_path):
    path = tmp_path / "nested" / "dir" / "tasks.json"
    store.save(path, [])
    assert path.exists()


def test_load_returns_empty_list_on_empty_file(tmp_path):
    path = tmp_path / "tasks.json"
    path.write_text("[]")
    assert store.load(path) == []
