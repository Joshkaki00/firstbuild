# /verify — Full verification pipeline

Run all four verification steps in order. Stop and report the first failure. Do not proceed past a failing step.

```bash
cd /Volumes/T9/dev/firstbuild
```

## Step 1: Import check

Verify all modules import without errors:

```bash
PYTHONPATH=src python3 -c "import task_cli.store; import task_cli.tasks; import task_cli.cli; print('✓ imports OK')"
```

**Pass:** prints `✓ imports OK`, exit code 0.  
**Fail:** any ImportError or ModuleNotFoundError. Report which import failed and stop.

## Step 2: Linter check

```bash
PYTHONPATH=src python3 -m py_compile src/task_cli/store.py src/task_cli/tasks.py src/task_cli/cli.py src/task_cli/__main__.py && echo "✓ syntax OK"
```

If `ruff` or `flake8` is installed, also run:
```bash
ruff check src/ 2>/dev/null || flake8 src/ 2>/dev/null || echo "(no linter installed, skipping style check)"
```

**Pass:** no syntax errors reported.  
**Fail:** report the file and line number of each error and stop.

## Step 3: Test check

```bash
PYTHONPATH=src python3 -m pytest tests/ -v 2>&1
```

**Pass:** all tests pass (look for `N passed` with 0 failed).  
**Fail:** report which tests failed and their assertion errors. Stop here — do not run coverage until tests pass.

## Step 4: Coverage check

```bash
PYTHONPATH=src python3 -m pytest tests/ --cov=src --cov-report=term-missing -q 2>&1
```

**Pass:** `store.py` and `tasks.py` show 100% coverage.  
**Note:** `cli.py` and `__main__.py` will show 0% — this is expected (subprocess tests are not instrumented). Do not treat this as a failure.  
**Fail:** if `store.py` or `tasks.py` drop below 100%, report the missing lines.

## Summary report

After all steps, print a summary:

```
Step 1 — Import check:   PASS / FAIL
Step 2 — Linter check:   PASS / FAIL
Step 3 — Test check:     PASS (N tests) / FAIL (N failed)
Step 4 — Coverage check: PASS (store 100%, tasks 100%) / FAIL
```
