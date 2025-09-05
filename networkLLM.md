## **NetworkLLM: Intent-Aware Intrusion Detection Using Large Language Models Grounded in Protocol Semantics**

## **Abstract**

Traditional intrusion detection systems (IDS), such as Snort and Suricata, rely on signature-based or statistical anomaly detection, often failing to interpret the **semantic intent** behind network traffic. As adversaries exploit legitimate protocols in novel ways—for instance, through DNS tunneling or TLS padding exploits—these systems struggle to detect sophisticated attacks or explain their malicious purpose. **NetworkLLM introduces a novel framework that treats network protocols as a structured "language," with its own grammar (protocol specifications) and content (field semantics).** It leverages **Large Language Models (LLMs)** to translate this "network language" into human-readable intent narratives (e.g., "this packet is probing a server"). Unlike existing LLM-based IDS approaches that focus on anomaly detection or protocol parsing [1, 2, 3], NetworkLLM combines **field-aware tokenization**, **RFC-grounded Retrieval-Augmented Generation (RAG)**, and **LLM-guided fuzzing** to infer fine-grained intent classes (e.g., benign handshake, probe, exfiltration) and map them to adversarial tactics (e.g., MITRE ATT&CK). This enables an **explainable, intent-aware IDS** that not only identifies suspicious packets but also articulates their purpose, significantly enhancing Security Operations Center (SOC) efficiency and trust.

---

## **Background and Motivation**

### **The Gap in Existing Systems**
Current IDS solutions, including signature-based, statistical, and ML-based systems, are proficient at detecting anomalies or predefined signatures but lack the ability to reason about the **semantic intent** of network traffic. For example, the BenignIDS framework (v1.0.26) uses TF-IDF and tree-based models to classify traffic as normal or attack but does not interpret the specific malicious purpose of an attack packet, such as probing or exfiltration [4]. As cyber threats evolve, adversaries increasingly misuse legitimate protocols—such as using encrypted traffic for command-and-control—to evade byte-level or statistical detection. This creates a critical gap: existing systems answer "**what is anomalous?**" but not "**what is the traffic trying to achieve?**"

### **The Opportunity with LLMs**
By framing network protocols as a "language" with grammar defined by RFCs (e.g., protocol state machines) and content in field values and payloads, LLMs can interpret packets as structured messages, similar to sentences in human language. This approach allows NetworkLLM to translate network traffic into actionable, human-readable intent narratives (e.g., "this DNS packet is tunneling data"), providing SOC analysts with essential context. Unlike traditional ML methods or other LLM-based IDS that prioritize a binary outcome of anomaly detection [1, 3], NetworkLLM focuses on **multi-class intent inference and narrative explanation** grounded in protocol semantics, thereby bridging the gap between technical detection and human understanding.

### **Research Context and Differentiation**
While recent advancements (2024–2025) have highlighted the potential of LLMs in network security, NetworkLLM’s focus on translating network intent into human-readable narratives distinguishes it from existing work:
* **TrafficLLM (arXiv 2025):** Uses domain-specific tokenization for anomaly detection [1]. NetworkLLM extends this by tokenizing protocol fields for semantic structure and translating intents into narratives, moving beyond simple anomaly scores.
* **PROSPER (HotNets 2023):** Extracts protocol state machines from RFCs [2]. NetworkLLM builds on this by integrating RFC-based RAG for real-time intent grounding, which ensures explanations are aligned with protocol standards and mitigates LLM hallucinations.
* **ChatAFL (NDSS 2024):** Employs LLM-guided fuzzing to test protocol implementations [5]. NetworkLLM adapts this methodology to explore protocol misuse scenarios and generate adversarial training data, focusing on **intent discovery** rather than implementation vulnerabilities.
* **Packet Field Tree (ACM SIGCOMM 2024):** Provides field-aware representations for protocol reverse-engineering [6]. NetworkLLM leverages similar tokenization but prioritizes intent inference and narrative translation, mapping packet behavior directly to adversarial tactics.
* **LLMcap (2024):** Explores self-supervised anomaly detection in PCAPs [3]. NetworkLLM goes further by classifying specific intent classes and providing narrative explanations, which greatly enhances SOC usability.
* **BenignIDS Notebook (v1.0.26):** Uses TF-IDF and traditional ML for binary classification [4]. NetworkLLM upgrades this by using semantic field-aware tokenization and LLMs for multi-class intent inference, leading to a significant leap in interpretability.

This project pioneers a paradigm shift toward an **intent-aware, explainable IDS** by treating network traffic as a translatable language, directly addressing key gaps in both academic prototypes and operational SOC needs.

---

## **Research Questions**
1. How can network protocols be tokenized as a “language” to capture both syntactic structure (protocol grammar) and semantic content (field intent) for LLM processing?
2. Can LLMs reliably classify fine-grained intent classes (e.g., benign handshake, probe, exploit, exfiltration, C2) and translate them into human-readable narratives?
3. How does RFC-grounded RAG improve the accuracy and explainability of intent inference while mitigating LLM hallucinations?
4. Can LLM-guided fuzzing autonomously explore protocol misuse scenarios to discover novel attack intents and enhance adversarial training?
5. How do narrative intent explanations impact SOC analysts’ efficiency, false positive reduction, and trust in automated IDS alerts?

---

## **Objectives**
* Develop a **field-aware tokenization framework** that treats network protocols as a “language” with grammar (RFC-defined rules) and content (field semantics), optimized for LLM-based intent inference.
* Train **two-tier LLMs:** a lightweight classifier (e.g., DistilBERT) for real-time intent detection and an encoder-decoder (e.g., T5-small) for narrative generation with RFC grounding.
* Integrate **RFC-based RAG** with finite state machine (FSM) validation to ground intent inferences in protocol semantics, ensuring accurate and explainable outputs.
* Implement **self-supervised anomaly models** for zero-day intent discovery, translating anomalous patterns into narrative descriptions.
* Adapt **LLM-guided fuzzing** to generate adversarial training data by exploring protocol misuse scenarios.
* **Integrate NetworkLLM into a tiered defense architecture**, placing it after traditional filtering stages (e.g., firewall, signature-based IDS) to reduce the computational burden.
* Integrate into **SOC pipelines** (e.g., Elastic, Wazuh) and evaluate narrative outputs for analyst efficiency and trust.

---

## **Methodology**

### **Network Language Tokenization**
NetworkLLM encodes packets and flows into tokens that capture both protocol structure and semantics. We treat fields as "words" and flows as "sentences." Tokens will include special markers for protocol types (e.g., `<PROTO:tcp>`), roles (e.g., `<ROLE:client>`), field names and values (e.g., `<TCP.SRC_PORT=53214>`), and state context (e.g., `<STATE:TCP/Handshake/1>`). Variable-length payloads are handled using Byte-Pair Encoding (BPE) subwords, segmented into fixed-length chunks to maintain semantic integrity, a method inspired by TrafficLLM’s tokenization but tailored for intent [1].  This transforms raw bytes into a structured "sentence," enabling LLMs to reason over protocol grammar (e.g., field order per RFCs) and content (e.g., anomalous flag combinations).

### **LLM Training Strategy**
Our **two-tier LLM approach** balances efficiency and expressiveness:
* **Tier-1 Classifier:** A lightweight model (e.g., DistilBERT or DeBERTa-small) for real-time intent classification, trained on binary malicious labels and fine-grained intent classes (e.g., handshake, probe, C2) using supervised learning with cross-entropy loss [3, 13].
* **Tier-2 Generator:** An encoder-decoder model (e.g., T5-small) for narrative generation, trained to produce human-readable explanations (e.g., "This TCP packet initiates a suspicious connection to port 445, likely probing for SMB vulnerabilities") using sequence-to-sequence loss [2].

Training stages include:
1.  **Pre-training:** Masked token modeling on unlabeled PCAPs to learn protocol structure [7].
2.  **Fine-tuning (Classification):** Supervised fine-tuning using Low-Rank Adaptation (LoRA) on intent-labeled datasets, requiring 10,000–50,000 samples for convergence. We'll mitigate this data challenge by leveraging existing benchmarks and data augmentation via fuzzing [4, 5].
3.  **Fine-tuning (Narrative):** Train T5-small on a custom dataset with intent labels and narrative annotations, created via a semi-automated annotation process involving initial labeling from benchmarks (e.g., UNSW-NB15) and refinement by security experts [4, 5].

### **RFC-RAG and FSM Validation**
The **RFC-grounded RAG system** indexes RFCs using a hybrid approach: BM25 for keyword-based retrieval and dense embeddings (e.g., via FAISS) for semantic search. This allows the model to retrieve specific, relevant sentences or paragraphs (≤800 characters) to reduce context overload [4]. For example, a TCP SYN packet’s intent might retrieve “Section 4.2 of RFC 793: SYN flags initiate connections.” Ambiguities (e.g., conflicting RFC versions) are resolved by prioritizing the latest RFC and using multi-retrieval fusion. **FSM validation** extracts state machines from retrieved RFCs (building on PROSPER's parsing) and checks packet sequences for valid transitions; mismatches trigger re-inference with augmented prompts to correct hallucinations [2, 4].

### **Datasets**
* **Benchmark Datasets:** CIC-IDS2017 and UNSW-NB15 for initial validation [4, 7].
* **Modern Datasets:** MAWIFlow 2025, Gotham 2025, and CESNET-TimeSeries 2025 to evaluate complex scenarios [8, 9, 10].
* **Specialized Datasets:** BCCC-DarkNet-2025 and LLMPot ICS honeypot traces for niche domains [11, 12].
* **Custom Dataset:** A novel dataset of PCAPs annotated with fine-grained intent classes and human-readable narrative descriptions to train and evaluate narrative generation.

### **Zero-Day Detection and Fuzzing Loop**
A **self-supervised anomaly detector** (e.g., contrastive learning or autoencoders) will identify unusual flows by flagging high reconstruction errors, indicating potential zero-day intents [3]. These anomalies will then serve as “seeds” for **LLM-guided fuzzing**, which explores neighboring protocol states by mutating packet fields (e.g., altering TCP flags or payload entropy). This process adapts ChatAFL’s approach for intent discovery rather than bug detection [5]. Fuzzing outputs are then integrated as adversarial training samples, forming a **closed loop that enhances robustness and coverage of novel attack patterns** [7, 8].

### **Risks and Mitigations**
| Risk | Mitigation |
| :--- | :--- |
| **Computational Cost** | **Tiered defense architecture:** NetworkLLM will be deployed after traditional filtering stages (e.g., firewall, signature-based IDS, BenignIDS) to reduce the volume of traffic requiring advanced analysis. This ensures that the LLM only processes traffic that has bypassed initial defenses [4]. |
| **Hallucination** | **Schema-constrained outputs** requiring RFC citations; FSM validation ensures protocol compliance [2, 4]. |
| **Prompt Injection** | **No free-form prompts**; allow-list RAG sources (e.g., RFCs) and sanitize inputs via anomaly checks [6, 16]. |
| **Adversarial Traffic** | **Adversarial training** with fuzzed and red-teamed samples; include poisoned data to counter evasion [5, 16]. |

### **Operational Evaluation**
The operational impact will be quantified through a phased evaluation:
* **Retrospective Testing:** Evaluate on historical SOC PCAPs, measuring **false positive reduction** (target: 50%) against BenignIDS baselines [4, 9].
* **Shadow Deployment:** Test with 2–3 analysts in a simulated SOC environment, measuring **mean time to triage (MTTT)** (target: <5 minutes per alert) [9].
* **Pilot Study:** Conduct a trial with 6–10 analysts, collecting **trust ratings** via Likert-scale surveys and rationale clarity scores, comparing NetworkLLM's narrative alerts to anomaly-based alerts [9, 10].

---

## **Work Packages (36 Months)**
1. **Representation Learning (Months 1–6):** Develop a tokenizer for protocol semantics, ablating against TF-IDF [4, 6].
2. **Intent Inference (Months 6–12):** Fine-tune LLMs for intent classification and narrative generation [1].
3. **Grounded Explainability (Months 12–18):** Build the RFC-RAG system with FSM validation [2].
4. **Zero-Day Detection (Months 18–24):** Develop self-supervised models for novel intent discovery [3].
5. **Exploration & Robustness (Months 24–30):** Adapt LLM-guided fuzzing for protocol misuse discovery [5].
6. **Operational Deployment (Months 30–36):** Integrate into a tiered defense architecture and SOC tools, evaluating narrative outputs with analysts [4].

---

## **Evaluation Metrics**
* **Detection:** Precision-Recall AUC (PR-AUC), F1-score, ROC-AUC for intent classification accuracy.
* **Explainability:** Percentage of correct RFC citations, hallucination rate, and narrative coherence (e.g., BLEU score).
* **Exploration:** Protocol state coverage and number of novel intent classes discovered.
* **Operational:** **False positive reduction (target: 50%)**, **trust ratings**, and **MTTT (target: <5 minutes)**, measured in a pilot study.

---

## **Expected Contributions**
* A **novel IDS framework** that translates packet intent into narratives, enhancing SOC usability.
* A **field-aware tokenization method** optimized for protocol semantics, advancing beyond TF-IDF approaches [4].
* An **RFC-grounded RAG system** with FSM validation, reducing hallucinations [1].
* An **LLM-guided fuzzing methodology** for discovering protocol misuse intents, distinct from bug-focused fuzzing [5].
* A **deployment-ready SOC prototype** within a tiered defense architecture, improving on binary classification systems [4].
* A **theoretical framework** for defining network intent as a translatable language, bridging NLP and cybersecurity.

---

## **Timeline (36 Months)**
* **Year 1:** Develop the tokenization framework, establish baselines, and train the initial LLM classifier.
* **Year 2:** Implement RFC-RAG grounding, self-supervised anomaly detection with narrative translation, and the fuzzing harness.
* **Year 3:** Integrate into SOC tools within a tiered defense architecture, evaluate narrative outputs with analysts, and complete the thesis.

---

## **Impact**
* **Academic:** Advances the integration of NLP and cybersecurity, targeting high-impact venues like NDSS, ACM SIGCOMM, and IEEE S&P [13].
* **Industrial:** Enhances SOC automation with narrative-based alerts, reducing false positives and improving analyst trust [1, 3, 14].
* **Societal:** Strengthens cybersecurity resilience against zero-day exploits and protocol misuse, addressing ethical AI concerns with explainable, narrative-driven outputs, aligned with the OWASP LLM Top 10 (2025) [14, 15].

---

## **References**
(The references remain the same as provided.)
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
