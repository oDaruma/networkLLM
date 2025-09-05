
from __future__ import annotations
import pandas as pd

FIELD_PREFIXES = ("ip.", "tcp.", "udp.", "dns.", "http.", "tls.", "smb.", "modbus.", "dnp3.")

def row_to_tokens(row: pd.Series) -> str:
    toks = []
    for k, v in row.items():
        k_l = str(k).lower()
        if any(k_l.startswith(pref) for pref in FIELD_PREFIXES):
            toks.append(f"[{k_l}={v}]")
    return " ".join(map(str, toks))

def df_to_corpus(df: pd.DataFrame) -> pd.Series:
    return df.apply(row_to_tokens, axis=1)
