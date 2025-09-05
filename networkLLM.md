# NetworkLLM: Intent-Aware Intrusion Detection Using Large Language Models Grounded in Protocol Semantics

## Abstract

Traditional intrusion detection systems (IDS), such as Snort and Suricata, rely on signature-based or statistical anomaly detection, which struggle to interpret the semantic intent behind network traffic. As adversaries exploit legitimate protocols in novel ways (e.g., DNS tunneling, TLS padding exploits), these systems often fail to detect sophisticated attacks or explain their malicious purpose. **NetworkLLM introduces a novel framework that treats network protocols as a structured “language” with grammar (protocol specifications) and content (field semantics), leveraging Large Language Models (LLMs) to translate this “network language” into human-readable intent narratives (e.g., “this packet is probing a server”). Unlike existing LLM-based IDS approaches that focus on anomaly detection or protocol parsing [1, 2, 3], NetworkLLM combines field-aware tokenization, RFC-grounded Retrieval-Augmented Generation (RAG), and LLM-guided fuzzing to infer fine-grained intent classes (e.g., benign handshake, probe, exfiltration) and map them to adversarial tactics (e.g., MITRE ATT&CK). This enables an explainable, intent-aware IDS that not only identifies suspicious packets but articulates their purpose, enhancing Security Operations Center (SOC) efficiency and trust.**

## Background and Motivation

### Gap in Existing Systems
Current IDS solutions, including Snort, Suricata, and machine learning-based systems, excel at detecting anomalies or predefined signatures but lack the ability to reason about the semantic intent of network traffic. For example, the BenignIDS framework (v1.0.26) uses TF-IDF and tree-based models (e.g., LightGBM, XGBoost) to classify traffic as normal or attack but does not interpret why an attack packet serves a specific malicious purpose, such as probing or exfiltration [4]. As cyber threats evolve, adversaries increasingly misuse legitimate protocols (e.g., encrypted traffic for command-and-control), evading byte-level or statistical detection. This creates a critical gap: existing systems answer “what is anomalous?” but not “what is the traffic trying to achieve?”

### Opportunity with LLMs
By treating network protocols as a “language” with grammar (RFC-defined rules, e.g., protocol state machines) and content (field values and payloads), LLMs can interpret packets as structured messages, akin to sentences in human language. This enables NetworkLLM to translate network traffic into human-readable intent narratives (e.g., “this DNS packet is tunneling data”), providing SOC analysts with actionable, explainable alerts. Unlike traditional ML approaches (e.g., BenignIDS’s binary classification) or other LLM-based IDS that prioritize anomaly detection [1, 3], NetworkLLM emphasizes multi-class intent inference and narrative explanation, grounded in protocol semantics, to bridge the gap between technical detection and human understanding.

### Research Context and Differentiation
Recent advancements in 2024–2025 highlight the potential of LLMs in network security, but NetworkLLM’s focus on translating network intent into human-readable narratives sets it apart:
- **TrafficLLM (arXiv 2025)** uses domain-specific tokenization to process network flows, improving anomaly detection over raw bytes [1]. NetworkLLM extends this by tokenizing protocol fields to capture semantic structure and translating intents into human-readable narratives, rather than stopping at anomaly scores.
- **PROSPER (HotNets 2023)** extracts protocol state machines from RFCs, focusing on specification parsing [2]. NetworkLLM builds on this by integrating RFC-based RAG for real-time intent grounding, ensuring explanations align with protocol standards and reducing LLM hallucinations.
- **ChatAFL (NDSS 2024)** employs LLM-guided fuzzing to test protocol implementations [5]. NetworkLLM adapts fuzzing to explore protocol misuse scenarios and generate adversarial training data, focusing on intent discovery rather than implementation vulnerabilities.
- **Packet Field Tree (ACM SIGCOMM 2024)** provides field-aware representations for protocol reverse-engineering [6]. NetworkLLM leverages similar tokenization but prioritizes intent inference and narrative translation over reverse-engineering, mapping packet behavior to adversarial tactics.
- **LLMcap (2024)** explores self-supervised anomaly detection in PCAPs [3]. NetworkLLM goes beyond anomaly detection to classify specific intent classes and provide narrative explanations, enhancing SOC usability.
- **BenignIDS Notebook (v1.0.26)** uses TF-IDF and ML models for binary classification on UNSW-NB15 [4]. NetworkLLM replaces TF-IDF with field-aware tokenization, employs LLMs for multi-class intent inference, and adds narrative translation, significantly advancing interpretability.

This project pioneers a paradigm shift toward intent-aware, explainable IDS by treating network traffic as a translatable language, addressing gaps in both academic prototypes and operational SOC needs.

## Research Questions
1. How can network protocols be tokenized as a “language” to capture both syntactic structure (protocol grammar) and semantic content (field intent) for LLM processing?
2. Can LLMs reliably classify fine-grained intent classes (e.g., benign handshake, probe, exploit, exfiltration, C2) and translate them into human-readable narratives?
3. How does RFC-grounded RAG improve the accuracy and explainability of intent inference while mitigating LLM hallucinations?
4. Can LLM-guided fuzzing autonomously explore protocol misuse scenarios to discover novel attack intents and enhance adversarial training?
5. How do narrative intent explanations impact SOC analysts’ efficiency, false positive reduction, and trust in automated IDS alerts?

## Objectives
- Develop a **field-aware tokenization framework** that treats network protocols as a “language” with grammar (RFC-defined rules) and content (field semantics), optimized for LLM-based intent inference.
- Train **two-tier LLMs**: a lightweight classifier (e.g., DistilBERT) for real-time intent detection and an encoder-decoder (e.g., T5-small) for narrative generation with RFC grounding.
- Integrate **RFC-based RAG** with finite state machine (FSM) validation to ground intent inferences in protocol semantics, ensuring accurate and explainable outputs.
- Implement **self-supervised anomaly models** for zero-day intent discovery, translating anomalous patterns into narrative descriptions.
- Adapt **LLM-guided fuzzing** for generating adversarial training data by exploring protocol misuse scenarios.
- Integrate into **SOC pipelines** (e.g., Elastic, Wazuh) and evaluate narrative outputs for analyst efficiency and trust.

## Methodology
### Network Language Tokenization
**NetworkLLM encodes packets and flows into tokens that capture protocol structure and semantics, treating fields as “words” and flows as “sentences.” Tokens include special markers for protocol types (e.g., `<PROTO:tcp>`), roles (e.g., `<ROLE:client>`), field names and values (e.g., `<TCP.SRC_PORT=53214>`), and state context (e.g., `<STATE:TCP/Handshake/1>`). Variable-length payloads are handled using byte-pair encoding (BPE) subwords, segmented into fixed-length chunks (e.g., 512 bytes) to maintain semantic integrity, inspired by TrafficLLM’s tokenization but tailored for intent [1].**

**Example: TCP SYN packet tokenization**
```
<PROTO:tcp> <ROLE:client> <IP.SRC=10.0.0.5> <IP.DST=10.0.0.8> <TCP.SRC_PORT=53214> <TCP.DST_PORT=445> <TCP.FLAG=SYN> <LEN=66> <ENTROPY=0.2> <STATE:TCP/Handshake/1>
```
**This transforms raw bytes into a structured “sentence,” enabling LLMs to reason over protocol grammar (e.g., field order per RFCs) and content (e.g., anomalous flag combinations). For variable-length payloads, BPE ensures semantic preservation, with padding or truncation for oversized payloads, balancing detail and model constraints [1].**

### LLM Training Strategy
**A two-tier LLM approach balances efficiency and expressiveness:**
- **Tier-1 Classifier**: A lightweight model (e.g., DistilBERT or DeBERTa-small) for real-time intent classification, trained on binary malicious labels and multi-class intent labels (e.g., handshake, probe, C2) using supervised learning with cross-entropy loss [3, 13].
- **Tier-2 Generator**: An encoder-decoder model (e.g., T5-small) for narrative generation, trained to produce human-readable explanations (e.g., “This TCP packet initiates a suspicious connection to port 445, likely probing for SMB vulnerabilities”) using sequence-to-sequence loss [2].
**Training stages include:**
1. **Pre-training**: Masked token modeling on unlabeled PCAPs (e.g., CIC-IDS2017) to learn protocol structure [7].
2. **Fine-tuning (Classification)**: Supervised fine-tuning using Low-Rank Adaptation (LoRA) on intent-labeled datasets, requiring 10,000–50,000 samples for convergence, mitigated by transfer learning from cybersecurity-pretrained LLMs (e.g., BERTector) [13, 14].
3. **Fine-tuning (Narrative)**: Train T5-small on a custom dataset with intent labels and narrative annotations, created via semi-automated annotation: initial labels from benchmarks (e.g., UNSW-NB15), refined by 5–10 security experts for narrative quality, augmented with fuzzing-generated variants [4, 5].
**Challenges include the need for large labeled datasets; we’ll mitigate by leveraging existing benchmarks and data augmentation via fuzzing [5].**

### RFC-RAG and FSM Validation
**The RFC-grounded RAG system indexes RFCs using a hybrid approach: BM25 for keyword-based retrieval and dense embeddings (e.g., via FAISS) for semantic search, retrieving specific sentences or paragraphs (≤800 characters) rather than entire sections to reduce context overload [4]. For example, a TCP SYN packet’s intent might retrieve “Section 4.2 of RFC 793: SYN flags initiate connections.” Ambiguities (e.g., conflicting RFC versions) are resolved by prioritizing the latest RFC and using multi-retrieval fusion to combine relevant snippets. FSM validation extracts state machines from retrieved RFCs (building on PROSPER’s parsing) and checks packet sequences for valid transitions; mismatches (e.g., invalid state jumps) trigger re-inference with augmented prompts to correct hallucinations [2, 4].**

### Datasets
- **Benchmark Datasets**: CIC-IDS2017 and UNSW-NB15 for initial validation of intent classification, leveraging their established attack labels and compatibility with BenignIDS’s preprocessing [4, 7].
- **Modern Datasets**: MAWIFlow 2025 (flow-based realistic traffic), Gotham 2025 (large-scale IoT traffic), and CESNET-TimeSeries 2025 (encrypted traffic time series) to evaluate intent inference in complex scenarios [8, 9, 10].
- **Specialized Datasets**: BCCC-DarkNet-2025 (encrypted darknet traffic) and LLMPot ICS honeypot traces (industrial control system emulation) for intent discovery in niche domains [11, 12].
- **Custom Dataset**: A novel dataset of PCAPs annotated with fine-grained intent classes (e.g., handshake, probe, C2) and human-readable narrative descriptions, created through semi-automated annotation and expert refinement, to train and evaluate narrative generation.

### Zero-Day Detection and Fuzzing Loop
**The self-supervised anomaly detector (e.g., contrastive learning or autoencoders) identifies unusual flows by high reconstruction errors, flagging potential zero-day intents [3]. These anomalies serve as “seeds” for LLM-guided fuzzing, which explores neighboring protocol states by mutating packet fields (e.g., altering TCP flags or payload entropy) to confirm or discover new intents, adapting ChatAFL’s approach for intent discovery rather than bug detection [5]. Fuzzing outputs are integrated as adversarial training samples, forming a closed loop that enhances robustness and coverage of novel attack patterns [7, 8].**

### Risks and Mitigations
**The following risks and mitigations address LLM-specific challenges:**

| Risk                | Mitigation                                          |
|--------------------|----------------------------------------------------|
| **Computational Cost** | **Two-tier pipeline**: Lightweight DistilBERT for initial classification, escalating to T5-small for narrative generation on suspicious packets; quantization and batch processing on GPUs target <1s per packet latency [6]. |
| **Hallucination**     | **Schema-constrained outputs** requiring RFC citations; FSM validation ensures protocol compliance [2, 4]. |
| **Prompt Injection**  | **No free-form prompts**; allow-list RAG sources (e.g., RFCs, curated datasets) and sanitize inputs via anomaly checks [6, 16]. |
| **Adversarial Traffic** | **Adversarial training** with fuzzed and red-teamed samples; include poisoned data in training to counter evasion [5, 16]. |

### Operational Evaluation
**Operational impact will be quantified through:**
- **Retrospective Testing**: Evaluate on historical SOC PCAPs (e.g., from Elastic/Wazuh), measuring false positive reduction (target: 50% via narrative context) against BenignIDS baselines [4, 9].
- **Shadow Deployment**: Test with 2–3 analysts in a simulated SOC environment, measuring mean time to triage (MTTT; target: <5 minutes per alert) using logged interactions in tools like Splunk or ELK Stack [9].
- **Pilot Study**: Conduct a trial with 6–10 analysts, collecting trust ratings via Likert-scale surveys (e.g., “How clear is the narrative?”) and rationale clarity scores, comparing NetworkLLM’s narrative alerts to anomaly-based alerts [9, 10].

### Work Packages (36 Months)
1. **Representation Learning (Months 1–6)**: Develop a tokenizer that encodes protocol fields as “words” and flows as “sentences,” optimized for intent semantics, ablating against TF-IDF (as in BenignIDS) [4, 6].
2. **Intent Inference (Months 6–12)**: Fine-tune LLMs for intent classification and narrative generation, unlike TrafficLLM’s anomaly focus [1].
3. **Grounded Explainability (Months 12–18)**: Build an RFC-RAG index with FSM validation, extending PROSPER’s static parsing to dynamic intent grounding [2].
4. **Zero-Day Detection (Months 18–24)**: Develop self-supervised models to detect novel intents, translating anomalies into narratives, unlike LLMcap’s anomaly-only focus [3].
5. **Exploration & Robustness (Months 24–30)**: Adapt ChatAFL’s fuzzing for protocol misuse scenarios, feeding anomalies into the fuzzer for intent discovery [5].
6. **Operational Deployment (Months 30–36)**: Integrate into SOC tools, evaluating narrative outputs for analyst trust, extending BenignIDS’s deployment focus [4].

## Evaluation Metrics
- **Detection**: Precision-Recall AUC (PR-AUC), F1-score, ROC-AUC for intent classification accuracy across imbalanced classes.
- **Explainability**: Percentage of correct RFC citations, hallucination rate (via manual or automated checks), and narrative coherence (e.g., BLEU score for text quality).
- **Exploration**: Protocol state coverage, number of novel intent classes or vulnerabilities discovered.
- **Operational**: **False positive reduction (target: 50%), trust ratings (via Likert-scale surveys), and MTTT (target: <5 minutes), measured in a pilot with 6–10 analysts using SOC tools [9, 10].**

## Expected Contributions
- A **novel IDS framework** that translates network protocol “language” into human-readable intent narratives, enhancing SOC usability and interpretability.
- A **field-aware tokenization method** optimized for protocol semantics, advancing beyond TF-IDF approaches like BenignIDS [4].
- An **RFC-grounded RAG system** with FSM validation, reducing hallucinations compared to generic LLM-IDS approaches like TrafficLLM [1].
- A **LLM-guided fuzzing methodology** for discovering protocol misuse intents, distinct from ChatAFL’s bug-focused fuzzing [5].
- A **deployment-ready SOC prototype** with narrative alerts, improving on BenignIDS’s binary classification and SHAP explanations [4].
- A **theoretical framework** for defining network intent as a translatable language, bridging NLP and cybersecurity.

## Timeline (36 Months)
- **Year 1**: Develop tokenization framework, establish baselines (extending BenignIDS’s preprocessing and models), and train initial LLM classifier for intent inference [4].
- **Year 2**: Implement RFC-RAG grounding, self-supervised anomaly detection with narrative translation, and fuzzing harness for intent discovery.
- **Year 3**: Integrate into SOC tools (e.g., Elastic, Wazuh), evaluate narrative outputs with analysts, and complete thesis.

## Impact
- **Academic**: Advances NLP and cybersecurity integration by framing network protocols as a translatable language, targeting high-impact venues like NDSS, ACM SIGCOMM, and IEEE S&P [13].
- **Industrial**: Enhances SOC automation with narrative-based alerts, reducing false positives and improving analyst trust, unlike anomaly-focused systems like TrafficLLM or LLMcap [1, 3, 14].
- **Societal**: Strengthens cybersecurity resilience against zero-day exploits and protocol misuse, addressing ethical AI concerns with explainable, narrative-driven outputs, aligning with OWASP LLM Top 10 (2025) [14, 15].

## References
1. TrafficLLM: Domain-Specific Tokenization for Network Traffic Analysis, arXiv, 2025.
2. PROSPER: Extracting Protocol State Machines from RFCs, HotNets, 2023.
3. LLMcap: Self-Supervised Anomaly Detection in PCAPs, 2024.
4. BenignIDS_Trainer_v1.0.26: Label-Agnostic Bayesian Optimisation IDS, Imperial College London, 2025.
5. ChatAFL: LLM-Guided Fuzzing for Protocol Testing, NDSS, 2024.
6. Packet Field Tree: Field-Aware Representations for Protocol Reverse-Engineering, ACM SIGCOMM, 2024.
7. CIC-IDS2017: Intrusion Detection Dataset, University of New Brunswick, 2017.
8. MAWIFlow 2025: Flow-Based Traffic Dataset, 2025.
9. Gotham 2025: Large-Scale IoT Traffic Dataset, 2025.
10. CESNET-TimeSeries 2025: Encrypted Traffic Time Series Dataset, 2025.
11. BCCC-DarkNet-2025: Encrypted Darknet Traffic Dataset, 2025.
12. LLMPot: ICS Honeypot Traces, 2025.
13. NDSS: Network and Distributed System Security Symposium, 2024–2025.
14. OWASP Top 10 for LLM Applications, 2025.
15. Anthropic: AI Misuse Countermeasures, 2025.
16. Adversarial Machine Learning, NIST, 2025.
