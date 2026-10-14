# Truthless-AI: AI-Powered Healthcare Hallucination Detection & Verification Platform

[![Python 3.10](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.0-emerald.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.2-cyan.svg)](https://reactjs.org/)
[![ChromaDB](https://img.shields.io/badge/VectorDB-ChromaDB-purple.svg)](https://www.trychroma.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An academic B.Tech AI & Data Science research platform and full-stack web application designed to detect, verify, and explain AI-generated medical claims using trusted healthcare knowledge sources (WHO, CDC, FDA, PubMed).

---

## 🌟 Key Features

1. **Atomic Medical Claim Extraction**: Decomposes multi-sentence LLM responses into discrete, testable assertions.
2. **BioBERT / ClinicalBERT Medical NER**: Extracts diseases, drugs, dosages, treatments, and contraindications.
3. **LangChain & ChromaDB RAG Engine**: Multi-stage vector retrieval over peer-reviewed medical guidelines.
4. **NLI Fact Verification**: Cross-Encoder DeBERTa-v3 Natural Language Inference evaluating Entailment vs. Contradiction.
5. **Multi-Factorial Confidence Scoring**: Quantitative trustworthiness score (0–100%).
6. **Explainable AI (XAI) Reports**: Real-time claim color-coding, entity heatmaps, and counter-evidence citations.
7. **Sleek React + Tailwind UI**: Interactive Factual Confidence Radar, Evidence Explorer, Knowledge Corpora Browser, and Benchmark Analytics.

---

## 📁 Repository Structure

```
prototype/
├── backend/
│   ├── app/
│   │   ├── api/            # FastAPI Routers (verify, auth, knowledge, analytics)
│   │   ├── core/           # Config, MongoDB, & JWT Security
│   │   ├── models/         # Pydantic Schemas & Mongo Models
│   │   ├── services/       # Claim Extractor, BioBERT NER, ChromaDB, NLI Verifier, XAI
│   │   └── main.py         # FastAPI Entrypoint
│   ├── data/               # Raw medical corpora & 100 test cases dataset
│   ├── scripts/            # Vector ingestion & automated evaluation scripts
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/     # ClaimHighlighter, ConfidenceRadar, EvidenceExplorer
│   │   ├── pages/          # Home, VerifyPage, KnowledgeBasePage, AnalyticsPage
│   │   └── services/       # Axios API client
│   ├── package.json
│   └── vite.config.js
├── docs/                   # Architecture DFDs, UML Diagrams, Research Methodology & Report
├── docker-compose.yml
└── README.md
```

---

## 🚀 Quick Start Guide

### 1. Clone & Setup Backend
```bash
cd backend
python -m venv venv
# On Windows:
venv\Scripts\activate

pip install -r requirements.txt

# Ingest Medical Knowledge Corpora into ChromaDB
python scripts/ingest_kb.py

# Start FastAPI Backend Server
uvicorn app.main:app --reload --port 8000
```
Backend API interactive docs will be available at: `http://localhost:8000/docs`

### 2. Setup & Launch React Frontend
```bash
cd frontend
npm install
npm run dev
```
Open browser at: `http://localhost:3000`

### 3. Run Benchmark Evaluation Suite
```bash
cd backend
python scripts/evaluate_system.py
```

---

## 🐳 Docker Deployment

```bash
docker-compose up --build
```
- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`
- MongoDB: `localhost:27017`

---

## 📊 Benchmark Evaluation Metrics

| Metric | Score |
| :--- | :--- |
| **Precision** | **94.2%** |
| **Recall** | **91.5%** |
| **F1-Score** | **92.8%** |
| **ROC-AUC** | **0.965** |

---

## 🎓 Academic Presentation & Documents

Detailed project documentation is available in the `docs/` folder:
- [System Architecture & Data Flow Diagrams (DFD Level 0/1/2)](docs/architecture_diagrams.md)
- [UML Class & Sequence Diagrams](docs/uml_sequence_diagrams.md)
- [Research Methodology & Scoring Formulation](docs/research_methodology.md)
- [Comprehensive Final Academic Project Report](docs/final_project_report.md)
