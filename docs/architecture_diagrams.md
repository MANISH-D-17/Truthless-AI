# System Architecture & Data Flow Diagrams (DFD)

## 1. System Architecture Diagram

```mermaid
flowchart TD
    subgraph Client ["Frontend Layer (React.js + Tailwind CSS)"]
        UI[User / Clinician Interface]
        INP[Query & LLM Response Input]
        HEAT[Claim Highlighter & BioBERT Entity Heatmap]
        RADAR[Factual Confidence Radar]
        EXP[RAG Evidence & Source Explorer]
    end

    subgraph Gateway ["API Gateway Layer (FastAPI)"]
        API[FastAPI Router / REST Endpoint]
        AUTH[JWT Security & Auth Handler]
    end

    subgraph Pipeline ["AI Processing & Verification Pipeline"]
        EXT[Claim Extraction Module]
        NER[BioBERT Medical Entity Recognition]
        EMB[SentenceTransformer Embeddings]
        NLI[Cross-Encoder DeBERTa-v3 NLI Engine]
        SCORE[Multi-Factorial Confidence Scorer]
        XAI[Explainable Report Generator]
    end

    subgraph Storage ["Persistence & Knowledge Base Layer"]
        CHROMA[(ChromaDB Vector Store)]
        KB[(WHO / CDC / FDA / PubMed Guidelines)]
        MONGO[(MongoDB Audit Database)]
    end

    UI --> INP
    INP --> API
    API --> AUTH
    API --> EXT
    EXT --> NER
    EXT --> EMB
    EMB --> CHROMA
    CHROMA <--> KB
    CHROMA --> NLI
    NER --> NLI
    NLI --> SCORE
    SCORE --> XAI
    XAI --> MONGO
    XAI --> API
    API --> HEAT
    API --> RADAR
    API --> EXP
```

---

## 2. Data Flow Diagrams (DFD)

### DFD Level 0 (Context Diagram)

```mermaid
graph TD
    User([Healthcare User / Clinician]) <-->|1. Input Query & LLM Output / 4. Verified Report| Platform[AI Healthcare Hallucination Detection Platform]
    KnowledgeBase[(WHO / CDC / FDA / PubMed Guidelines)] -->|2. Trusted Medical Passages| Platform
    AuditLog[(MongoDB Database)] <-->|3. Persistence Audit Logs| Platform
```

### DFD Level 1 (Macro Process Breakdown)

```mermaid
graph TD
    User([User]) -->|1. Raw Input| P1[Process 1.0: Claim & Entity Extraction]
    P1 -->|Extracted Claims & BioBERT Tags| P2[Process 2.0: RAG Vector Retrieval]
    KnowledgeBase[(ChromaDB Corpora)] -->|Top-K Evidence| P2
    P2 -->|Claims + Evidence| P3[Process 3.0: NLI Fact Verification Engine]
    P3 -->|Stance Scores| P4[Process 4.0: Confidence Scoring & XAI Generation]
    P4 -->|Audit Record| MongoDB[(MongoDB Audit Logs)]
    P4 -->|Visual Verification Report| User
```

### DFD Level 2 (Detailed Fact Verification Sub-process)

```mermaid
graph TD
    Claims[Extracted Atomic Claim] --> P3_1[3.1 Premise-Hypothesis Formatter]
    Evidence[Retrieved Evidence Passages] --> P3_1
    P3_1 --> P3_2[3.2 DeBERTa Cross-Encoder Inference]
    P3_2 --> P3_3{3.3 Stance Classifier}
    P3_3 -->|Entailment > 0.55| Verdict1[SUPPORTS - Verified]
    P3_3 -->|Contradiction > 0.45| Verdict2[REFUTES - Hallucinated]
    P3_3 -->|Inconclusive| Verdict3[NOT_ENOUGH_INFO - Neutral]
    Verdict1 --> P3_4[3.4 Conflicting Evidence Resolver]
    Verdict2 --> P3_4
    Verdict3 --> P3_4
```
