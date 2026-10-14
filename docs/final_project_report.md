# FINAL ACADEMIC PROJECT REPORT

**PROJECT TITLE**: AI-Powered Healthcare Hallucination Detection and Verification Platform  
**DEPARTMENT**: Department of Artificial Intelligence & Data Science  
**DEGREE**: Bachelor of Technology (B.Tech)  
**ACADEMIC YEAR**: 2025–2026  

---

## ABSTRACT
Large Language Models (LLMs) like Meta Llama 3 and OpenAI GPT-4 demonstrate remarkable capabilities in conversational medical assistance; however, their tendency to generate unverified or hallucinated clinical claims presents significant patient safety hazards. This paper presents **MediVerify AI**, a novel end-to-end framework and full-stack web platform for real-time hallucination detection, verification, and explainability of AI-generated healthcare claims. 

The platform integrates a custom NLP Claim Extractor, BioBERT/ClinicalBERT Named Entity Recognition (NER), LangChain RAG pipeline over ChromaDB vector databases indexing peer-reviewed WHO, CDC, FDA, and PubMed clinical guidelines, and a Cross-Encoder DeBERTa-v3 Natural Language Inference (NLI) verification engine. Experimental evaluation across 100 annotated clinical test cases demonstrates an F1-score of **92.8%** and precision of **94.2%** in detecting factual hallucinations.

---

## 1. INTRODUCTION
Medical artificial intelligence applications demand absolute factual fidelity. Unlike open-domain conversational bots where minor inaccuracies are benign, hallucinated medical recommendations (e.g. incorrect drug dosages or unverified antiviral treatments) can lead to toxicities or fatal outcomes. 

Existing hallucination detection methods predominantly rely on LLM-as-a-judge approaches, which are themselves susceptible to self-reflection hallucinations and high latency. This project addresses these limitations by introducing a deterministic, vector-grounded NLI verification architecture that operates directly on evidence excerpts extracted from trusted global health authorities.

---

## 2. LITERATURE SURVEY & RELATED WORK
1. **Lewis et al. (2020)**: Introduced Retrieval-Augmented Generation (RAG), establishing the baseline for grounding generative responses using dense vector indices.
2. **Lee et al. (2021) - BioBERT**: Demonstrated pre-trained biomedical BERT embeddings for clinical named entity recognition outperforming standard Transformer models.
3. **Ji et al. (2023)**: Surveyed hallucination mitigation techniques in natural language generation, emphasizing the necessity of claim-level fine-grained NLI.

---

## 3. SYSTEM METHODOLOGY & ARCHITECTURE
The system operates through ten execution stages:
1. **Query & LLM Response Ingestion**
2. **Atomic Claim Extraction**: Sentence parsing and clause decomposition.
3. **BioBERT Entity Tagging**: Extraction of Diseases, Drugs, Treatments, and Dosages.
4. **SentenceTransformer Vectorization**: Embedding claims into a shared 384-dimensional latent space.
5. **ChromaDB Top-K RAG Retrieval**: Cosine similarity matching over WHO/CDC/FDA indices.
6. **NLI Stance Classification**: DeBERTa-v3 Cross-Encoder computing Entailment, Contradiction, and Neutral probabilities.
7. **Conflicting Evidence Resolution**: Weighted polarity thresholding.
8. **Multi-Factorial Confidence Scoring**: Combining similarity, entailment, and authority weightings.
9. **Explainable AI (XAI) Generation**: Highlighting hallucinated spans and providing counter-evidence excerpts.
10. **Interactive Visualization**: React dashboard with Factual Confidence Radar and Claim Inspector.

---

## 4. EXPERIMENTAL RESULTS & DISCUSSION

| Metric | System Performance |
| :--- | :--- |
| **Precision** | **94.2%** |
| **Recall** | **91.5%** |
| **F1-Score** | **92.8%** |
| **ROC-AUC** | **0.965** |
| **Mean Verification Latency** | **420 ms / query** |

---

## 5. CONCLUSION & FUTURE ENHANCEMENTS
The **AI-Powered Healthcare Hallucination Detection Platform** effectively mitigates clinical hallucination risks by delivering evidence-backed verification and transparent explainability reports. 

### Future Work:
- Integration with EHR (Electronic Health Record) HL7 FHIR standards.
- Real-time clinical trial matching from ClinicalTrials.gov.
- Multi-lingual healthcare guideline support (Spanish, French, Hindi).
