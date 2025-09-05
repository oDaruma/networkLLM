# networkLLM — Intent-Aware Intrusion Detection with LLMs

**What this does**  
- Reproducible scaffold to infer **packet/flow intent** (benign vs malicious) using LLMs grounded by protocol semantics.
- Includes a **LightGBM baseline**, **field-aware LLM classifier**, RFC **RAG** module, and evaluation harness (PR-AUC/F1).

**Why**  
- Traditional IDS focus on signatures. This project surfaces **intended behaviour** (handshake, probe, exploit, exfiltration) and provides **explanations** grounded in RFCs/specs.

## Directory layout
```
networkLLM_full/
├─ src/networkllm/
│  ├─ config.py                 # Sanity Config — single source of truth
│  ├─ preprocess/
│  │  ├─ zeek.py                # Zeek/Wireshark JSON loaders
│  │  ├─ tokenise.py            # Field-aware tokenisation → LLM text
│  │  └─ preprocessor.py        # Derive preprocessor + feature lists
│  ├─ representations/
│  │  └─ field_text.py          # Bytes-aware helpers (entropy, length)
│  ├─ models/
│  │  ├─ baseline_lgbm.py       # Baseline LightGBM (tabular flows)
│  │  └─ llm_classifier.py      # DistilBERT classifier over tokens
│  ├─ eval/
│  │  └─ metrics.py             # Metrics passthrough
│  └─ rag/
│     └─ spec_index.py          # Minimal FAISS index for RFC RAG
├─ examples/
│  ├─ run_baseline.py           # Train baseline and print report
│  └─ run_llm_intent.py         # Train LLM classifier and print report
├─ data/                        # Place CSVs/JSON here
├─ staging/                     # Manifests and intermediate artefacts
├─ out/                         # Models, reports, charts
├─ requirements.txt
└─ LICENSE
```

## Quickstart
1. Create a Python 3.12+ environment, `pip install -r requirements.txt`.
2. Place a labelled CSV under `data/` (e.g., CIC-IDS2017/UNSW-NB15/MAWIFlow export).
3. Edit `src/networkllm/config.py` only (single source of truth) to set `DATA_PATH`, `TARGET_COL`, `stage_root`.
4. Baseline: `python -m networkllm.models.baseline_lgbm`
5. LLM intent: `python examples/run_llm_intent.py`

**Conventions (Imperial naming):** `X_train/y_train`, `X_val/y_val`, `X_test/y_test`; `feature_names`, `cat_cols`, `num_cols`; `baseline_model`, `bayes`; `RANDOM_STATE`, `DATA_PATH`, `TARGET_COL`, `stage_root`.
