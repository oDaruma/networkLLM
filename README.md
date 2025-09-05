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

---

## Other related researchs

| Paper / Project                                      | Dataset(s) Used                               | Method                                             | Key Results                                                      | Implications for **networkLLM**                                                                                       |
| ---------------------------------------------------- | --------------------------------------------- | -------------------------------------------------- | ---------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| **LLM-Guided Protocol Fuzzing (ChatAFL, NDSS 2024)** | Real protocol parsers (e.g., FTP, SMTP, HTTP) | LLM extracts grammar + generates seeds for fuzzing | Higher **coverage**, new states found, escaped coverage plateaus | Use LLMs not just for detection, but for **hard-negative generation** (augment training with fuzzed malicious seeds). |
| **PROSPER (HotNets 2023)**                           | RFCs (TLS, DNS, HTTP)                         | LLM extracts FSMs from specs                       | Accurate state machines built from RFC text                      | Ground intent detection in **RFC-derived state transitions**; enables “violates RFC section X” explanations.          |
| **Packet Field Tree (ACM 2024)**                     | Open traces + crafted protocols               | Hybrid learning of field hierarchies               | Better field extraction accuracy vs heuristics                   | Adopt **field-aware tokenisation** (e.g., `[tcp.dst_port=445]`) for LLM input; avoids raw hex ambiguity.              |
| **LLMcap (2024)**                                    | PCAP traces (network failures/anomalies)      | Self-supervised LLM anomaly detection              | Outperformed statistical anomaly baselines                       | LLMs can **detect unseen threats** without labels; useful for zero-day scenarios.                                     |
| **TrafficLLM (2025)**                                | CIC-IDS2017, UNSW-NB15 + custom tokenisation  | Domain-specific tokenisation + fine-tuning         | Higher classification accuracy, more stable on imbalance         | Validates **tokenisation strategy** in `networkLLM`: combine field-tokens with byte-level features.                   |
| **Arkko (ANRW 2024)**                                | Raw socket/packet traces                      | Direct LLM application to low-level traffic        | Struggled on raw bytes, better on diagnostic narratives          | Reinforces: preprocess packets → **structured text** before LLM; avoid raw binary input.                              |
| **LLMPot (ICS Honeypot, 2024)**                      | ICS traffic (Modbus, DNP3)                    | LLM-generated honeypot responses                   | More realistic, intent-driven responses than rule-based          | LLMs capture **intent semantics**, useful for both IDS explanations and deception tools.                              |

---

## 🔑 Key Take-aways for **networkLLM**

* **Must:** Build on **field-aware tokens** (Packet Field Tree + TrafficLLM).
* **Should:** Add **RFC/RAG grounding** (PROSPER) for explainable alerts.
* **May:** Use **LLM-guided fuzzing (ChatAFL)** to mine hard negatives and augment training.
* **Can:** Leverage **LLMcap-style anomaly detection** for unlabeled traffic (zero-day hunting).
* **Avoid:** Feeding raw packet bytes (Arkko) → always normalise first.
* **Explore:** Extending intent detection into **active deception** (LLMPot-style honeypots).

---



