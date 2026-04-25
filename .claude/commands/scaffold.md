# /scaffold — Generate test file stubs for a new feature

Use this before starting any new feature. It creates the three test files needed for the red phase across all layers.

## Arguments

The user provides a feature name in snake_case, e.g.: `/scaffold tags` or `/scaffold due_date`

Call the feature name `$FEATURE` in all output below.

## What to generate

Create three files. Do not implement any logic — stubs only. Each file should be ready for the developer to fill in the failing tests.

### 1. `tests/test_tasks_$FEATURE.py`

```python
"""Tests for $FEATURE support in tasks.py — domain-agent lane. Written before implementation."""
import pytest
from task_cli import tasks


# TODO: add failing tests for $FEATURE domain logic
# Pattern: def test_<behavior>(): ...
```

### 2. `tests/test_store_$FEATURE.py`

```python
"""Tests verifying store persists $FEATURE field — store-agent lane."""
from task_cli import store


# TODO: verify $FEATURE field survives a save/load roundtrip
# Reminder: store is schema-agnostic — these tests should pass without store changes
# Pattern:
# def test_$FEATURE_field_survives_roundtrip(tmp_path):
#     path = tmp_path / "tasks.json"
#     tasks = [{"id": 1, "description": "Test", "status": "todo", "$FEATURE": <value>}]
#     store.save(path, tasks)
#     loaded = store.load(path)
#     assert loaded[0]["$FEATURE"] == <value>
```

### 3. `tests/test_cli_$FEATURE.py`

```python
"""Tests for $FEATURE flag in CLI — cli-agent lane. Written before implementation."""
import json
import os
import subprocess
import sys
from pathlib import Path

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


# TODO: add failing CLI tests for $FEATURE
# Pattern: def test_<command>_with_$FEATURE(tmp_path): ...
```

## After creating the files

1. Run `PYTHONPATH=src python3 -m pytest tests/test_tasks_$FEATURE.py tests/test_store_$FEATURE.py tests/test_cli_$FEATURE.py -v` to confirm they collect 0 tests (stubs only — that's correct at this stage).
2. Tell the developer: "Stubs created. Fill in the failing tests, then run `/tdd $FEATURE` to start the red/green/refactor cycle."
3. Do NOT write any implementation code.
