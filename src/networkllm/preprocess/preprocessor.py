
from __future__ import annotations
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from ..config import TARGET_COL

def derive_preprocessor(df: pd.DataFrame):
    cat_cols = [c for c in df.columns if df[c].dtype == "object" and c != TARGET_COL]
    num_cols = [c for c in df.columns if c not in cat_cols + [TARGET_COL]]
    preprocessor = ColumnTransformer([
        ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
        ("num", StandardScaler(), num_cols),
    ])
    feature_names = cat_cols + num_cols
    return preprocessor, feature_names, cat_cols, num_cols
