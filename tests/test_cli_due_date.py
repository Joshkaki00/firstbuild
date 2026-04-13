"""Tests for --due flag in CLI — cli-agent lane. Written before implementation."""
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

PYTHON = sys.executable
CLI = [PYTHON, "-m", "task_cli"]
ENV_KEY = "TASK_CLI_FILE"


def run(*args, task_file: Path) -> subprocess.CompletedProcess:
    env = {**os.environ, ENV_KEY: str(task_file)}
    return subprocess.run(
        [*CLI, *args],
        capture_output=True,
        text=True,
        env=env,
        cwd=Path(__file__).parent.parent / "src",
    )


def test_add_with_due_date_saves_field(tmp_path):
    tf = tmp_path / "tasks.json"
    result = run("add", "File taxes", "--due", "2026-04-20", task_file=tf)
    assert result.returncode == 0
    tasks = json.loads(tf.read_text())
    assert tasks[0]["due_date"] == "2026-04-20"


def test_add_without_due_date_saves_none(tmp_path):
    tf = tmp_path / "tasks.json"
    run("add", "Buy milk", task_file=tf)
    tasks = json.loads(tf.read_text())
    assert tasks[0].get("due_date") is None


def test_add_invalid_due_date_exits_nonzero(tmp_path):
    result = run("add", "Bad task", "--due", "not-a-date", task_file=tmp_path / "tasks.json")
    assert result.returncode != 0


def test_list_shows_due_date_in_output(tmp_path):
    tf = tmp_path / "tasks.json"
    run("add", "File taxes", "--due", "2026-04-20", task_file=tf)
    result = run("list", task_file=tf)
    assert "2026-04-20" in result.stdout


def test_list_without_due_date_does_not_crash(tmp_path):
    tf = tmp_path / "tasks.json"
    run("add", "Buy milk", task_file=tf)
    result = run("list", task_file=tf)
    assert result.returncode == 0
    assert "Buy milk" in result.stdout
