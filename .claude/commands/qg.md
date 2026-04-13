# /qg — Verify all quality gates from spec.md

Run through all 3 quality gates defined in `spec.md` against a temporary task file so no real data is touched.

```bash
export TASK_CLI_FILE=/tmp/qg-tasks.json
rm -f $TASK_CLI_FILE

echo "--- QG-1: Add and List ---"
python -m task_cli add "Write tests"
python -m task_cli list

echo "--- QG-2: Complete a Task ---"
python -m task_cli add "Mark me done"
python -m task_cli done 1
python -m task_cli list
python -m task_cli done 999   # should exit 1

echo "--- QG-3: Delete a Task ---"
python -m task_cli add "Delete me"
python -m task_cli delete 2
python -m task_cli list
python -m task_cli delete 999  # should exit 1

rm -f $TASK_CLI_FILE
```

## Success criteria

- QG-1: both commands exit 0; `list` shows the task with ID, status, and description.
- QG-2: `done 1` exits 0 and `list` shows `done` status; `done 999` exits 1 with an error message.
- QG-3: `delete 2` exits 0 and `list` no longer shows that task; `delete 999` exits 1 with an error message.

Report PASS or FAIL for each gate. If any gate fails, describe what was wrong.
