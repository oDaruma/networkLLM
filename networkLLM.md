# NetworkLLM: Intent-Aware Intrusion Detection Using Large Language Models Grounded in Protocol Semantics

## Abstract

Traditional intrusion detection systems (IDS) are constrained by their reliance on signatures or statistical anomaly detection, which often fail to capture the intent behind network traffic. As cyber threats evolve, adversaries increasingly exploit legitimate protocols in semantically novel ways (e.g., DNS tunnelling, TLS padding exploits), evading byte-level detection.

This PhD project proposes NetworkLLM, a framework that employs Large Language Models (LLMs) to infer the semantic intent of network packets and flows. By combining field-aware tokenisation, RFC-grounded retrieval, and LLM-guided exploration, the system will move from surface anomaly spotting towards intent-aware, explainable detection. The outcome will be an IDS capable of recognising not only that a packet is suspicious, but why, grounded in protocol semantics, and mapping it to adversarial tactics (e.g., MITRE ATT&CK).

## Background and Motivation

### Gap in Existing Systems
Existing IDS solutions, such as Snort, Suricata, and machine learning-based detectors, primarily identify anomalies or predefined signatures but lack deep semantic reasoning. They can detect "what is odd?" but struggle to explain "what was the traffic trying to achieve?" This limitation becomes critical in modern threats where attackers use legitimate protocols creatively, such as in encrypted traffic or protocol misuse.

### Opportunity with LLMs
LLMs, trained on structured representations, can interpret packets as natural language-like messages, enabling intent inference (e.g., distinguishing a benign handshake from an exploit attempt). This leverages the models' ability to reason over context and semantics.

### Research Context
Recent advancements support this shift:
- LLM-guided fuzzing, such as ChatAFL (NDSS 2024), demonstrates that LLMs can learn protocol grammars and generate meaningful traffic for testing.
- PROSPER (HotNets 2023) shows LLMs can extract protocol state machines from RFC documents, aiding in semantic understanding.
- TrafficLLM (arXiv 2025) introduces domain-specific tokenisation that enhances LLM performance over raw byte analysis for network traffic.
- LLMcap (2024) explores self-supervised LLMs for anomaly detection in unlabeled PCAP files (though specific implementations may vary). (Note: This appears to be an emerging concept; further validation needed.)
- Packet Field Tree (ACM SIGCOMM 2024) provides a hybrid approach for field-aware representations in protocol reverse-engineering.

These developments indicate a paradigm shift towards intent-aware intrusion detection, blending NLP techniques with cybersecurity.

## Research Questions

1. How can network traffic be represented as language-like tokens that capture both byte-level robustness and semantic field structure?
2. Can LLMs reliably infer intent classes (e.g., benign handshake, probe, exploit, exfiltration, C2 communication)?
3. How does grounding LLMs in RFC/state machine knowledge improve accuracy and reduce hallucinations?
4. Can LLMs autonomously explore protocol space (via fuzzing) to discover new attack behaviours and generate adversarial training data?
5. How do intent-aware IDS outputs impact SOC analysts’ efficiency, false positive rates, and trust in automated alerts?

## Objectives

- Develop a field-aware tokenisation framework for network traffic, optimised for LLM input.
- Train and evaluate intent classifiers using LLMs (e.g., fine-tuned DistilBERT or domain-adapted models) on tokenised traffic.
- Integrate RFC-based Retrieval-Augmented Generation (RAG) for explainable IDS decisions.
- Build a self-supervised anomaly detector for zero-day intent discovery in unlabeled data.
- Implement LLM-guided fuzzing to stress-test the system and generate adversarial training samples.
- Demonstrate operational integration in Security Operations Center (SOC) pipelines, such as Elastic or Wazuh.

## Methodology

### Datasets
- **Benchmark Datasets**: CIC-IDS2017 and UNSW-NB15 for initial validation of intrusion detection models.
- **Modern Datasets**: MAWIFlow 2025 (flow-based realistic traffic for intrusion evaluation). Gotham 2025 (large-scale IoT network traffic for security research). CESNET TimeSeries 2025 (encrypted traffic time series for anomaly detection).
- **Specialised Datasets**: BCCC-DarkNet-2025 (encrypted traffic for darknet and threat analysis). LLMPot ICS honeypot traces (LLM-based honeypots for industrial control systems emulation).

### Work Packages (36 Months)
1. **Representation Learning (Months 1–6)**: Design and ablate field-aware tokenisers (e.g., inspired by Packet Field Tree) versus raw byte encodings.
2. **Intent Inference (Months 6–12)**: Fine-tune LLMs on tokenised datasets to classify intents; evaluate multi-class performance.
3. **Grounded Explainability (Months 12–18)**: Construct an RFC/spec RAG index (building on PROSPER); incorporate finite state machine (FSM) validation to mitigate hallucinations.
4. **Zero-Day Detection (Months 18–24)**: Develop self-supervised models (e.g., autoencoders or contrastive learning) for anomaly spotting in PCAPs.
5. **Exploration & Robustness (Months 24–30)**: Adapt LLM-guided fuzzing (e.g., from ChatAFL) to generate novel attacks and hard negatives for training.
6. **Operational Deployment (Months 30–36)**: Integrate into SOC tools; conduct human-in-the-loop studies with analysts.

### Evaluation Metrics
- **Detection**: Precision-Recall AUC (PR-AUC), F1-score, ROC-AUC, focusing on imbalanced classes.
- **Explainability**: Percentage of correct RFC citations, hallucination rate (via manual or automated checks).
- **Exploration**: Protocol state coverage, number of new paths or vulnerabilities discovered.
- **Operational**: Reduction in analyst false positives, trust ratings (surveys), mean time to triage alerts.

## Expected Contributions
- A novel intent-aware IDS framework leveraging LLMs for semantic packet analysis.
- An optimised field-aware traffic representation for LLM processing.
- An RFC-grounded explanation system to enhance reliability in AI-driven IDS.
- A methodology for LLM-guided fuzzing and adversarial hard-negative mining in cybersecurity.
- A deployment-ready prototype for SOC integration.
- A theoretical framework for defining and evaluating "network intent" in cybersecurity contexts.

## Timeline (3 Years)
- **Year 1**: Establish baselines, develop tokenisation framework, and build initial LLM classifier.
- **Year 2**: Implement RFC-RAG grounding, anomaly detection module, and fuzzing harness.
- **Year 3**: Focus on SOC integration, analyst evaluations, and thesis completion.

## Impact
- **Academic**: Bridges NLP, cybersecurity, and formal methods, fostering interdisciplinary research.
- **Industrial**: Enhances SOC automation, reduces alert fatigue, and improves explainability for threat hunting.
- **Societal**: Strengthens cybersecurity resilience against zero-day exploits and adversarial tactics, promoting trust in automated systems.

This draft can be refined further based on specific requirements, such as adding budget details, supervisor info, or expanding sections. If you need adjustments (e.g., more focus on ethics, risks, or feasibility), let me know!
