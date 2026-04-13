"""Tests for --priority flag in CLI — cli-agent lane. Written before implementation."""
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


def test_add_with_high_priority_saves_field(tmp_path):
    tf = tmp_path / "tasks.json"
    result = run("add", "Urgent thing", "--priority", "high", task_file=tf)
    assert result.returncode == 0
    tasks = json.loads(tf.read_text())
    assert tasks[0]["priority"] == "high"


def test_add_with_low_priority_saves_field(tmp_path):
    tf = tmp_path / "tasks.json"
    run("add", "Someday thing", "--priority", "low", task_file=tf)
    tasks = json.loads(tf.read_text())
    assert tasks[0]["priority"] == "low"


def test_add_without_priority_defaults_to_medium(tmp_path):
    tf = tmp_path / "tasks.json"
    run("add", "Normal thing", task_file=tf)
    tasks = json.loads(tf.read_text())
    assert tasks[0]["priority"] == "medium"


def test_add_invalid_priority_exits_nonzero(tmp_path):
    result = run("add", "Bad task", "--priority", "critical", task_file=tmp_path / "tasks.json")
    assert result.returncode != 0


def test_list_with_priority_filter_shows_only_matching(tmp_path):
    tf = tmp_path / "tasks.json"
    run("add", "High thing", "--priority", "high", task_file=tf)
    run("add", "Low thing", "--priority", "low", task_file=tf)
    result = run("list", "--priority", "high", task_file=tf)
    assert "High thing" in result.stdout
    assert "Low thing" not in result.stdout


def test_list_without_priority_filter_shows_all(tmp_path):
    tf = tmp_path / "tasks.json"
    run("add", "High thing", "--priority", "high", task_file=tf)
    run("add", "Low thing", "--priority", "low", task_file=tf)
    result = run("list", task_file=tf)
    assert "High thing" in result.stdout
    assert "Low thing" in result.stdout


def test_list_shows_priority_in_output(tmp_path):
    tf = tmp_path / "tasks.json"
    run("add", "Important", "--priority", "high", task_file=tf)
    result = run("list", task_file=tf)
    assert "high" in result.stdout


def test_list_with_invalid_priority_filter_exits_nonzero(tmp_path):
    result = run("list", "--priority", "urgent", task_file=tmp_path / "tasks.json")
    assert result.returncode != 0
