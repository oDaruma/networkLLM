# NetworkLLM: Intent-Aware Intrusion Detection Using Large Language Models Grounded in Protocol Semantics

## Abstract

Traditional intrusion detection systems (IDS), such as Snort and Suricata, rely on signature-based or statistical anomaly detection, which struggle to interpret the semantic intent behind network traffic. As adversaries exploit legitimate protocols in novel ways (e.g., DNS tunneling, TLS padding exploits), these systems often fail to detect sophisticated attacks or explain their malicious purpose. NetworkLLM introduces a novel framework that treats network protocols as a structured "language" with grammar (protocol specifications) and content (field semantics), leveraging Large Language Models (LLMs) to translate this "network language" into human-readable intent narratives (e.g., "this packet is probing a server"). Unlike existing LLM-based IDS approaches that focus on anomaly detection or protocol parsing, NetworkLLM combines field-aware tokenization, RFC-grounded Retrieval-Augmented Generation (RAG), and LLM-guided fuzzing to infer fine-grained intent classes (e.g., benign handshake, probe, exfiltration) and map them to adversarial tactics (e.g., MITRE ATT&CK). This enables an explainable, intent-aware IDS that not only identifies suspicious packets but articulates their purpose, enhancing Security Operations Center (SOC) efficiency and trust.

## Background and Motivation

### Gap in Existing Systems
Current IDS solutions, including Snort, Suricata, and machine learning-based systems like those in the BenignIDS notebook (v1.0.26), excel at detecting anomalies or predefined signatures but lack the ability to reason about the semantic intent of network traffic.<grok:render type="render_inline_citation"><argument name="citation_id">0</argument></grok:render> For example, the BenignIDS framework uses TF-IDF and tree-based models (e.g., LightGBM, XGBoost) to classify traffic as normal or attack but does not interpret why an attack packet serves a specific malicious purpose, such as probing or exfiltration.<grok:render type="render_inline_citation"><argument name="citation_id">0</argument></grok:render> As cyber threats evolve, adversaries increasingly misuse legitimate protocols (e.g., encrypted traffic for command-and-control), evading byte-level or statistical detection. This creates a critical gap: existing systems answer "what is anomalous?" but not "what is the traffic trying to achieve?"

### Opportunity with LLMs
By treating network protocols as a "language" with grammar (RFC-defined rules, e.g., protocol state machines) and content (field values and payloads), LLMs can interpret packets as structured messages, akin to sentences in human language. This enables NetworkLLM to translate network traffic into human-readable intent narratives (e.g., "this DNS packet is tunneling data"), providing SOC analysts with actionable, explainable alerts. Unlike traditional ML approaches (e.g., BenignIDS’s binary classification) or other LLM-based IDS that prioritize anomaly detection, NetworkLLM emphasizes multi-class intent inference and narrative explanation, grounded in protocol semantics, to bridge the gap between technical detection and human understanding.

### Research Context and Differentiation
Recent advancements highlight the potential of LLMs in network security, but NetworkLLM’s focus on translating network intent into human-readable narratives sets it apart:
- **TrafficLLM (arXiv 2025)** uses domain-specific tokenization to process network flows, improving anomaly detection over raw bytes. NetworkLLM extends this by tokenizing protocol fields to capture semantic structure and translating intents into human-readable narratives, rather than stopping at anomaly scores.<grok:render type="render_inline_citation"><argument name="citation_id">61</argument></grok:render>
- **PROSPER (HotNets 2023)** extracts protocol state machines from RFCs, focusing on specification parsing. NetworkLLM builds on this by integrating RFC-based RAG for real-time intent grounding, ensuring explanations align with protocol standards and reducing LLM hallucinations.<grok:render type="render_inline_citation"><argument name="citation_id">15</argument></grok:render><grok:render type="render_inline_citation"><argument name="citation_id">18</argument></grok:render>
- **ChatAFL (NDSS 2024)** employs LLM-guided fuzzing to test protocol implementations. NetworkLLM adapts fuzzing to explore protocol misuse scenarios and generate adversarial training data, focusing on intent discovery rather than implementation vulnerabilities.<grok:render type="render_inline_citation"><argument name="citation_id">51</argument></grok:render><grok:render type="render_inline_citation"><argument name="citation_id">52</argument></grok:render>
- **Packet Field Tree (ACM SIGCOMM 2024)** provides field-aware representations for protocol reverse-engineering. NetworkLLM leverages similar tokenization but prioritizes intent inference and narrative translation over reverse-engineering, mapping packet behavior to adversarial tactics.<grok:render type="render_inline_citation"><argument name="citation_id">70</argument></grok:render>
- **LLMcap (2024)** explores self-supervised anomaly detection in PCAPs. NetworkLLM goes beyond anomaly detection to classify specific intent classes and provide narrative explanations, enhancing SOC usability.<grok:render type="render_inline_citation"><argument name="citation_id">65</argument></grok:render>
- **BenignIDS Notebook (v1.0.26)** uses TF-IDF and ML models for binary classification on UNSW-NB15. NetworkLLM replaces TF-IDF with field-aware tokenization, employs LLMs for multi-class intent inference, and adds narrative translation, significantly advancing interpretability.<grok:render type="render_inline_citation"><argument name="citation_id">0</argument></grok:render>

This project pioneers a paradigm shift toward intent-aware, explainable IDS by treating network traffic as a translatable language, addressing gaps in both academic prototypes and operational SOC needs.

## Research Questions
1. How can network protocols be tokenized as a "language" to capture both syntactic structure (protocol grammar) and semantic content (field intent) for LLM processing?
2. Can LLMs reliably classify fine-grained intent classes (e.g., benign handshake, probe, exploit, exfiltration, C2) and translate them into human-readable narratives?
3. How does RFC-grounded RAG improve the accuracy and explainability of intent inference while mitigating LLM hallucinations?
4. Can LLM-guided fuzzing autonomously explore protocol misuse scenarios to discover novel attack intents and enhance adversarial training?
5. How do narrative intent explanations impact SOC analysts’ efficiency, false positive reduction, and trust in automated IDS alerts?

## Objectives
- Develop a field-aware tokenization framework that treats network protocols as a "language" with grammar (RFC-defined rules) and content (field semantics), optimized for LLM-based intent inference.
- Train LLMs (e.g., fine-tuned DistilBERT or domain-adapted models) to classify fine-grained intent classes and generate human-readable narrative explanations (e.g., "this packet is attempting data exfiltration").
- Integrate RFC-based RAG with finite state machine (FSM) validation to ground intent inferences in protocol semantics, ensuring accurate and explainable outputs.
- Build a self-supervised anomaly detector for zero-day intent discovery, translating anomalous patterns into narrative descriptions.
- Implement LLM-guided fuzzing to explore protocol misuse scenarios, generating adversarial training data for novel intent classes.
- Demonstrate operational integration in SOC pipelines (e.g., Elastic, Wazuh), evaluating narrative outputs for analyst efficiency and trust.

**Differentiation**: Unlike TrafficLLM’s focus on anomaly detection via tokenization,<grok:render type="render_inline_citation"><argument name="citation_id">61</argument></grok:render> NetworkLLM prioritizes multi-class intent classification and narrative translation. Compared to PROSPER’s static RFC parsing,<grok:render type="render_inline_citation"><argument name="citation_id">15</argument></grok:render> it dynamically grounds intents in RFCs for real-time explainability. Unlike ChatAFL’s fuzzing for implementation bugs,<grok:render type="render_inline_citation"><argument name="citation_id">51</argument></grok:render> it targets protocol misuse intents. It advances BenignIDS’s binary classification by using LLMs for nuanced intent narratives.<grok:render type="render_inline_citation"><argument name="citation_id">0</argument></grok:render>

## Methodology
### Datasets
- **Benchmark Datasets**: CIC-IDS2017 and UNSW-NB15 for initial validation of intent classification, leveraging their established attack labels and compatibility with BenignIDS’s preprocessing.<grok:render type="render_inline_citation"><argument name="citation_id">0</argument></grok:render>
- **Modern Datasets**: MAWIFlow 2025 (flow-based realistic traffic), Gotham 2025 (large-scale IoT traffic), and CESNET-TimeSeries 2025 (encrypted traffic time series) to evaluate intent inference in complex scenarios.<grok:render type="render_inline_citation"><argument name="citation_id">85</argument></grok:render><grok:render type="render_inline_citation"><argument name="citation_id">75</argument></grok:render><grok:render type="render_inline_citation"><argument name="citation_id">90</argument></grok:render>
- **Specialized Datasets**: BCCC-DarkNet-2025 (encrypted darknet traffic) and LLMPot ICS honeypot traces (industrial control system emulation) for intent discovery in niche domains.<grok:render type="render_inline_citation"><argument name="citation_id">80</argument></grok:render><grok:render type="render_inline_citation"><argument name="citation_id">45</argument></grok:render>
- **Custom Dataset**: A novel dataset of PCAPs annotated with fine-grained intent classes (e.g., handshake, probe, C2) and human-readable narrative descriptions to train and evaluate narrative generation.

### Work Packages (36 Months)
1. **Representation Learning (Months 1–6)**: Develop a tokenizer that encodes protocol fields as "words" and flows as "sentences," inspired by Packet Field Tree but optimized for intent semantics, ablating against TF-IDF (as in BenignIDS).<grok:render type="render_inline_citation"><argument name="citation_id">70</argument></grok:render><grok:render type="render_inline_citation"><argument name="citation_id">0</argument></grok:render>
2. **Intent Inference (Months 6–12)**: Fine-tune LLMs to classify intents (e.g., probe, exfiltration) and generate narrative explanations, unlike TrafficLLM’s anomaly focus.<grok:render type="render_inline_citation"><argument name="citation_id">61</argument></grok:render>
3. **Grounded Explainability (Months 12–18)**: Build an RFC-RAG index with FSM validation, extending PROSPER’s static parsing to dynamic intent grounding.<grok:render type="render_inline_citation"><argument name="citation_id">15</argument></grok:render>
4. **Zero-Day Detection (Months 18–24)**: Develop self-supervised models (e.g., contrastive learning) to detect novel intents, translating anomalies into narratives, unlike LLMcap’s anomaly-only focus.<grok:render type="render_inline_citation"><argument name="citation_id">65</argument></grok:render>
5. **Exploration & Robustness (Months 24–30)**: Adapt ChatAFL’s fuzzing to generate protocol misuse scenarios, focusing on intent discovery rather than bug detection.<grok:render type="render_inline_citation"><argument name="citation_id">51</argument></grok:render>
6. **Operational Deployment (Months 30–36)**: Integrate into SOC tools, evaluating narrative outputs for analyst trust, extending BenignIDS’s deployment focus with narrative explanations.<grok:render type="render_inline_citation"><argument name="citation_id">0</argument></grok:render>

### Evaluation Metrics
- **Detection**: Precision-Recall AUC (PR-AUC), F1-score, ROC-AUC for intent classification accuracy across imbalanced classes.
- **Explainability**: Percentage of correct RFC citations, hallucination rate (via manual or automated checks), and narrative coherence (e.g., BLEU score for text quality).
- **Exploration**: Protocol state coverage, number of novel intent classes or vulnerabilities discovered.
- **Operational**: Reduction in analyst false positives, trust ratings (via surveys), and mean time to triage for narrative-based alerts.

**Differentiation**: NetworkLLM’s methodology prioritizes intent narrative generation over TrafficLLM’s anomaly detection, PROSPER’s static parsing, or LLMcap’s unsupervised anomalies. It extends BenignIDS’s preprocessing and drift monitoring (Section 9.7) with LLM-driven intent translation and narrative outputs.<grok:render type="render_inline_citation"><argument name="citation_id">0</argument></grok:render><grok:render type="render_inline_citation"><argument name="citation_id">61</argument></grok:render><grok:render type="render_inline_citation"><argument name="citation_id">15</argument></grok:render><grok:render type="render_inline_citation"><argument name="citation_id">65</argument></grok:render>

## Expected Contributions
- A pioneering intent-aware IDS that translates network protocol "language" into human-readable intent narratives, enhancing SOC usability and interpretability.
- A field-aware tokenization framework optimized for protocol semantics and intent inference, advancing beyond TF-IDF approaches like BenignIDS.<grok:render type="render_inline_citation"><argument name="citation_id">0</argument></grok:render>
- An RFC-grounded RAG system with FSM validation, reducing hallucinations compared to generic LLM-IDS approaches like TrafficLLM.<grok:render type="render_inline_citation"><argument name="citation_id">61</argument></grok:render>
- A novel LLM-guided fuzzing methodology for discovering protocol misuse intents, distinct from ChatAFL’s bug-focused fuzzing.<grok:render type="render_inline_citation"><argument name="citation_id">51</argument></grok:render>
- A deployment-ready prototype with narrative outputs integrated into SOC pipelines, improving on BenignIDS’s binary classification and SHAP explanations.<grok:render type="render_inline_citation"><argument name="citation_id">0</argument></grok:render>
- A theoretical framework for defining network intent as a translatable language, bridging NLP and cybersecurity for interdisciplinary impact.

## Timeline (3 Years)
- **Year 1**: Develop tokenization framework, establish baselines (extending BenignIDS’s preprocessing and models), and train initial LLM classifier for intent inference.<grok:render type="render_inline_citation"><argument name="citation_id">0</argument></grok:render>
- **Year 2**: Implement RFC-RAG grounding, self-supervised anomaly detection with narrative translation, and fuzzing harness for intent discovery.
- **Year 3**: Integrate into SOC tools (e.g., Elastic, Wazuh), evaluate narrative outputs with analysts, and complete thesis.

## Impact
- **Academic**: Advances the integration of NLP and cybersecurity by framing network protocols as a translatable language, targeting high-impact venues like NDSS, ACM SIGCOMM, and IEEE S&P.<grok:render type="render_inline_citation"><argument name="citation_id">10</argument></grok:render><grok:render type="render_inline_citation"><argument name="citation_id">70</argument></grok:render>
- **Industrial**: Enhances SOC automation with narrative-based alerts, reducing false positives and improving analyst trust, unlike anomaly-focused systems like TrafficLLM or LLMcap.<grok:render type="render_inline_citation"><argument name="citation_id">39</argument></grok:render><grok:render type="render_inline_citation"><argument name="citation_id">61</argument></grok:render><grok:render type="render_inline_citation"><argument name="citation_id">65</argument></grok:render>
- **Societal**: Strengthens cybersecurity resilience against zero-day exploits and protocol misuse, addressing ethical AI concerns with explainable, narrative-driven outputs, aligning with 2025 standards like OWASP LLM Top 10.<grok:render type="render_inline_citation"><argument name="citation_id">21</argument></grok:render><grok:render type="render_inline_citation"><argument name="citation_id">39</argument></grok:render>
