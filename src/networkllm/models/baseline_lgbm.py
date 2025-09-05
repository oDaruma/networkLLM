
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import json
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import average_precision_score, f1_score, precision_recall_fscore_support
from lightgbm import LGBMClassifier
from ..config import RANDOM_STATE, TARGET_COL, PATHS
from ..utils_io import write_json
from ..preprocess.preprocessor import derive_preprocessor
from sklearn.pipeline import Pipeline

@dataclass
class Split:
    X_train: pd.DataFrame
    X_val: pd.DataFrame
    X_test: pd.DataFrame
    y_train: pd.Series
    y_val: pd.Series
    y_test: pd.Series
    feature_names: list[str]
    cat_cols: list[str]
    num_cols: list[str]

def prepare_splits(df: pd.DataFrame) -> Split:
    y = df[TARGET_COL].astype(int)
    X = df.drop(columns=[TARGET_COL])
    X_tr, X_tmp, y_tr, y_tmp = train_test_split(X, y, test_size=0.3, stratify=y, random_state=RANDOM_STATE)
    X_va, X_te, y_va, y_te = train_test_split(X_tmp, y_tmp, test_size=0.5, stratify=y_tmp, random_state=RANDOM_STATE)
    preprocessor, feature_names, cat_cols, num_cols = derive_preprocessor(df)
    preprocessor.fit(X_tr)
    return Split(X_tr, X_va, X_te, y_tr, y_va, y_te, feature_names, cat_cols, num_cols)

def train_and_eval(df: pd.DataFrame) -> dict:
    spl = prepare_splits(df)
    model = LGBMClassifier(class_weight="balanced", random_state=RANDOM_STATE, n_estimators=400, learning_rate=0.05, num_leaves=63)
    pipe = Pipeline([("prep", derive_preprocessor(df)[0]), ("clf", model)])
    pipe.fit(spl.X_train, spl.y_train)
    yv = pipe.predict_proba(spl.X_val)[:, 1]
    yt = pipe.predict_proba(spl.X_test)[:, 1]
    ap_val = average_precision_score(spl.y_val, yv)
    ap_test = average_precision_score(spl.y_test, yt)
    yv_cls = (yv >= 0.5).astype(int)
    yt_cls = (yt >= 0.5).astype(int)
    p_val, r_val, f1_val, _ = precision_recall_fscore_support(spl.y_val, yv_cls, average="binary", zero_division=0)
    p_test, r_test, f1_test, _ = precision_recall_fscore_support(spl.y_test, yt_cls, average="binary", zero_division=0)
    report = {
        "val": {"AP": ap_val, "precision": p_val, "recall": r_val, "F1": f1_val},
        "test": {"AP": ap_test, "precision": p_test, "recall": r_test, "F1": f1_test},
        "feature_names": spl.feature_names,
        "cat_cols": spl.cat_cols,
        "num_cols": spl.num_cols,
    }
    write_json(report, PATHS.out / "baseline_lgbm_report.json")
    return report

if __name__ == "__main__":
    csvs = sorted(Path(PATHS.data).glob("*.csv"))
    if not csvs:
        raise FileNotFoundError("Place a labelled CSV under data/ (e.g., CIC-IDS2017 flows).")
    df = pd.read_csv(csvs[0])
    rep = train_and_eval(df)
    print(json.dumps(rep, indent=2))
