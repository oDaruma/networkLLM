
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import average_precision_score, f1_score
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
import numpy as np
from ..config import RANDOM_STATE, TARGET_COL, PATHS
from ..utils_io import write_json
from ..preprocess.tokenise import df_to_corpus

MODEL_NAME = "distilbert-base-uncased"  # small, local-friendly

@dataclass
class DS:
    enc: dict
    y: np.ndarray
    def __len__(self): return len(self.y)
    def __getitem__(self, i):
        item = {k: v[i] for k, v in self.enc.items()}
        item["labels"] = int(self.y[i]); return item

def encode(tokenizer, texts, labels, max_len=512):
    enc = tokenizer(list(texts), truncation=True, padding=True, max_length=max_len)
    return enc, np.asarray(labels, dtype=np.int64)

def train_and_eval(df: pd.DataFrame, text_col: str | None = None) -> dict:
    texts = df[text_col] if text_col else df_to_corpus(df.drop(columns=[TARGET_COL], errors="ignore"))
    y = df[TARGET_COL].astype(int)
    X_tr, X_tmp, y_tr, y_tmp = train_test_split(texts, y, test_size=0.3, stratify=y, random_state=RANDOM_STATE)
    X_va, X_te, y_va, y_te = train_test_split(X_tmp, y_tmp, test_size=0.5, stratify=y_tmp, random_state=RANDOM_STATE)

    tok = AutoTokenizer.from_pretrained(MODEL_NAME)
    enc_tr, y_tr = encode(tok, X_tr, y_tr)
    enc_va, y_va = encode(tok, X_va, y_va)
    enc_te, y_te = encode(tok, X_te, y_te)

    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=2)
    args = TrainingArguments(
        output_dir=str(PATHS.staging / "llm_cls"),
        per_device_train_batch_size=16,
        per_device_eval_batch_size=32,
        num_train_epochs=2,
        learning_rate=2e-5,
        weight_decay=0.01,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        seed=RANDOM_STATE,
        logging_steps=25,
    )
    tr = Trainer(model=model, args=args, train_dataset=DS(enc_tr, y_tr), eval_dataset=DS(enc_va, y_va), tokenizer=tok)
    tr.train()

    # Evaluate
    import torch
    def probs(enc):
        # Build a dummy dataset of correct length by reusing one of the arrays for length
        n = len(next(iter(enc.values())))
        logits = tr.predict(DS(enc, np.zeros(n, dtype=np.int64))).predictions
        return torch.softmax(torch.tensor(logits), dim=1).numpy()[:,1]

    pv = probs(enc_va); pt = probs(enc_te)
    ap_val = average_precision_score(y_va, pv); ap_test = average_precision_score(y_te, pt)
    f1_val = f1_score(y_va, pv >= 0.5); f1_test = f1_score(y_te, pt >= 0.5)
    report = {"val": {"AP": ap_val, "F1": f1_val}, "test": {"AP": ap_test, "F1": f1_test}}
    write_json(report, PATHS.out / "llm_intent_report.json")
    return report

if __name__ == "__main__":
    csvs = sorted(Path(PATHS.data).glob("*.csv"))
    if not csvs:
        raise FileNotFoundError("Place a labelled CSV under data/.")
    df = pd.read_csv(csvs[0])
    rep = train_and_eval(df)
    print(json.dumps(rep, indent=2))
