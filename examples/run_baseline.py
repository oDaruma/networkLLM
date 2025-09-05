"""
Run the LightGBM baseline on the first CSV found under data/.
"""
import json
from pathlib import Path
import pandas as pd
from networkllm.models.baseline_lgbm import train_and_eval

if __name__ == "__main__":
    csvs = sorted(Path("data").glob("*.csv"))
    if not csvs:
        raise FileNotFoundError("Place a labelled CSV in data/.")
    df = pd.read_csv(csvs[0])
    rep = train_and_eval(df)
    print(json.dumps(rep, indent=2))
