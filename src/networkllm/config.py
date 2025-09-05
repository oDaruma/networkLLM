
from __future__ import annotations
from pathlib import Path
from dataclasses import dataclass

# ===== Sanity Config (single declaration) =====
RANDOM_STATE: int = 42
DATA_PATH: str = "data"           # root folder for datasets (pcaps/CSV/Zeek JSON)
TARGET_COL: str = "label"         # binary: 0/1 or "benign"/"malicious"
stage_root: str = "staging"       # folder for manifests and intermediates

# Derived constants
OUT_ROOT: str = "out"
PROJECT_ROOT = Path(__file__).resolve().parents[2]

@dataclass(frozen=True)
class Paths:
    project = PROJECT_ROOT
    data = PROJECT_ROOT / DATA_PATH
    staging = PROJECT_ROOT / stage_root
    out = PROJECT_ROOT / OUT_ROOT

PATHS = Paths()
