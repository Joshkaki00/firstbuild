# /test — Run full test suite with coverage

Run all tests and report coverage for the source modules.

```bash
cd /Volumes/T9/dev/firstbuild
PYTHONPATH=src python3 -m pytest tests/ -v --cov=src --cov-report=term-missing
```

Expected: all 41 tests pass. `store.py` and `tasks.py` should show 100% coverage. `cli.py` and `__main__.py` will show 0% — this is expected because CLI tests run via subprocess and are not instrumented by pytest-cov.

If any tests fail, report which test failed and what the assertion error was before making any changes.
