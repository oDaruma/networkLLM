
from __future__ import annotations
from pathlib import Path
import json
import pandas as pd

def load_zeek_json(json_path: Path) -> pd.DataFrame:
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    # Expect list of records; coerce to DataFrame
    return pd.json_normalize(data)

def load_folder(folder: Path) -> pd.DataFrame:
    frames = []
    for p in sorted(Path(folder).glob("*.json")):
        frames.append(load_zeek_json(p))
    if not frames:
        raise FileNotFoundError(f"No JSON files found under: {folder}")
    return pd.concat(frames, axis=0, ignore_index=True)
