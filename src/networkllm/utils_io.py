
from __future__ import annotations
from pathlib import Path
import json
from .config import PATHS

def write_json(obj, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, sort_keys=True)

def read_json(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
