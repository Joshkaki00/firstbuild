"""JSON persistence layer. All file I/O lives here."""
import json
from pathlib import Path


def load(path: Path) -> list[dict]:
    path = Path(path)
    if not path.exists():
        return []
    return json.loads(path.read_text())


def save(path: Path, tasks: list[dict]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(tasks, indent=2))
