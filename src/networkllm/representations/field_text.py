
from __future__ import annotations
import pandas as pd
import numpy as np

def byte_entropy(payload_bytes: bytes) -> float:
    if not payload_bytes:
        return 0.0
    counts = np.bincount(np.frombuffer(payload_bytes, dtype=np.uint8), minlength=256)
    probs = counts / counts.sum()
    nz = probs > 0
    return float(-(probs[nz] * np.log2(probs[nz])).sum())

def add_basic_features(df: pd.DataFrame, payload_col: str = "payload") -> pd.DataFrame:
    out = df.copy()
    if payload_col in out.columns:
        lens = out[payload_col].fillna(b"").apply(lambda b: len(b) if isinstance(b, (bytes, bytearray)) else 0)
        ents = out[payload_col].fillna(b"").apply(lambda b: byte_entropy(b if isinstance(b, (bytes, bytearray)) else b""))
    else:
        lens = 0
        ents = 0.0
    out["payload_len"] = lens
    out["payload_entropy"] = ents
    return out
