"""Tests for cli.py — argparse entry point. Written before implementation."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

PYTHON = sys.executable
CLI = [PYTHON, "-m", "task_cli"]
ENV_KEY = "TASK_CLI_FILE"


def run(*args, task_file: Path) -> subprocess.CompletedProcess:
    import os
    env = {**os.environ, ENV_KEY: str(task_file)}
    return subprocess.run(
        [*CLI, *args],
        capture_output=True,
        text=True,
        env=env,
        cwd=Path(__file__).parent.parent / "src",
    )


def test_add_exits_zero(tmp_path):
    result = run("add", "Buy milk", task_file=tmp_path / "tasks.json")
    assert result.returncode == 0


def test_add_prints_confirmation(tmp_path):
    result = run("add", "Buy milk", task_file=tmp_path / "tasks.json")
    assert "Buy milk" in result.stdout or "1" in result.stdout


def test_list_exits_zero_with_no_tasks(tmp_path):
    result = run("list", task_file=tmp_path / "tasks.json")
    assert result.returncode == 0


def test_list_shows_added_task(tmp_path):
    tf = tmp_path / "tasks.json"
    run("add", "Write tests", task_file=tf)
    result = run("list", task_file=tf)
    assert "Write tests" in result.stdout


def test_done_marks_task_complete(tmp_path):
    tf = tmp_path / "tasks.json"
    run("add", "Do something", task_file=tf)
    result = run("done", "1", task_file=tf)
    assert result.returncode == 0
    tasks = json.loads(tf.read_text())
    assert tasks[0]["status"] == "done"


def test_done_with_invalid_id_exits_nonzero(tmp_path):
    result = run("done", "999", task_file=tmp_path / "tasks.json")
    assert result.returncode != 0


def test_delete_removes_task(tmp_path):
    tf = tmp_path / "tasks.json"
    run("add", "Temporary", task_file=tf)
    result = run("delete", "1", task_file=tf)
    assert result.returncode == 0
    tasks = json.loads(tf.read_text())
    assert tasks == []


def test_delete_with_invalid_id_exits_nonzero(tmp_path):
    result = run("delete", "999", task_file=tmp_path / "tasks.json")
    assert result.returncode != 0


def test_list_shows_done_status(tmp_path):
    tf = tmp_path / "tasks.json"
    run("add", "Finish me", task_file=tf)
    run("done", "1", task_file=tf)
    result = run("list", task_file=tf)
    assert "done" in result.stdout
