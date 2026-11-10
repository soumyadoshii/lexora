# Lexora
### Agentic Regulatory Intelligence & Compliance Platform

Lexora is an AI-powered regulatory intelligence platform designed to help users navigate complex financial regulations through evidence-grounded question answering, document retrieval, and automated verification.

Built around regulatory documents published by the Reserve Bank of India (RBI) and Securities and Exchange Board of India (SEBI), Lexora combines Retrieval-Augmented Generation (RAG) with agentic verification workflows to deliver accurate, traceable, and context-aware regulatory insights.

Instead of relying solely on an LLM's internal knowledge, Lexora retrieves relevant regulatory provisions, evaluates supporting evidence, and generates responses with source-level citations. Its verification layer checks citation validity, identifies unsupported answers, and enables structured comparison of regulatory documents.

**100+ Regulatory Circulars | Hybrid RAG Pipeline | 3 Verification Capabilities | 150+ Evaluation Queries**

---

## Key Features

### 1. Regulatory Document Intelligence

- Ingestion and indexing of 100+ RBI and SEBI regulatory circulars.
- Document-aware processing for regulatory content.
- Searchable regulatory knowledge base.
- Contextual retrieval of relevant provisions and supporting passages.
- Source-level traceability for retrieved regulatory information.

### 2. Hybrid Retrieval Pipeline

Lexora combines semantic and keyword-based retrieval to improve the relevance of regulatory search results.

- **Semantic Search:** Uses vector embeddings to retrieve contextually relevant regulatory passages.
- **Keyword Search:** Identifies exact terminology, regulatory phrases, and domain-specific references.
- **Hybrid Retrieval:** Combines semantic and lexical search results to improve retrieval coverage.
- **Reranking:** Reorders retrieved passages based on their relevance to the user's query.
- **Context Assembly:** Supplies the most relevant evidence to the generation layer.

This approach helps address the limitations of relying exclusively on either vector similarity or keyword matching.

### 3. Agentic Verification System

Lexora incorporates three verification capabilities to improve answer reliability.

#### Citation Validation
- Checks whether generated citations correspond to retrieved regulatory sources.
- Validates supporting evidence against the retrieved document context.
- Improves traceability between generated answers and original circulars.

#### Unsupported-Answer Abstention
- Identifies questions that cannot be adequately answered using available regulatory evidence.
- Prevents unsupported responses from being presented as established regulatory facts.
- Encourages evidence-based answering rather than speculative generation.

#### Regulatory Document Comparison
- Compares regulatory documents and their relevant provisions.
- Identifies differences in regulatory requirements and document content.
- Helps users understand changes and distinctions across circulars.

### 4. Evidence-Grounded AI Responses

- Powered by the Gemini API.
- Answers generated using retrieved regulatory context.
- Source-level citations supporting regulatory claims.
- Context-aware response generation.
- Verification before presenting answers.
- Abstention when sufficient supporting evidence is unavailable.

### 5. Automated Evaluation Framework

Lexora includes an evaluation framework designed to assess the reliability of its regulatory question-answering pipeline.

- 150+ labeled evaluation queries.
- Automated evaluation tests.
- Retrieval and answer verification checks.
- Citation validation testing.
- Unsupported-answer handling.
- GitHub Actions integration for automated CI execution.

The evaluation framework helps identify regressions and maintain consistent behavior as the retrieval and agent workflows evolve.

---

## System Architecture

Lexora follows a modular architecture that separates document processing, retrieval, answer generation, and verification.

### High-Level Workflow

1. **Document Ingestion:** Regulatory circulars from RBI and SEBI are collected and processed.
2. **Document Processing:** Content is prepared for indexing and retrieval.
3. **Vector Indexing:** Embeddings are stored in PostgreSQL using Supabase and pgvector.
4. **Query Processing:** User questions are processed and prepared for retrieval.
5. **Hybrid Retrieval:** Semantic and keyword-based search retrieve relevant regulatory evidence.
6. **Reranking:** Retrieved passages are reordered according to relevance.
7. **Context Construction:** Relevant evidence is assembled for the generation model.
8. **Answer Generation:** Gemini generates responses grounded in the retrieved context.
9. **Agentic Verification:** Citation validation, unsupported-answer abstention, and document comparison capabilities improve response reliability.
10. **Response Delivery:** The user receives an answer supported by regulatory source references.

### Architecture Diagram

```text
             USER QUERY
                 |
                 v
        QUERY PROCESSING
                 |
                 v
       HYBRID RETRIEVAL
          /          \
         v            v
   SEMANTIC SEARCH  KEYWORD SEARCH
         \            /
          v          v
        RESULT MERGING
                 |
                 v
             RERANKING
                 |
                 v
         CONTEXT ASSEMBLY
                 |
                 v
          GEMINI API
                 |
                 v
       AGENTIC VERIFICATION
          /      |       \
         v       v        v
     CITATION  ABSTENTION DOCUMENT
     VALIDATION           COMPARISON
          \      |       /
                 v
       EVIDENCE-GROUNDED
             ANSWER
                 |
                 v
        SOURCE CITATIONS
```

---

## Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Backend Framework | FastAPI |
| LLM | Google Gemini API |
| AI Architecture | Agentic RAG |
| Retrieval | Hybrid Semantic & Keyword Search |
| Vector Database | PostgreSQL, Supabase, pgvector |
| Retrieval Optimization | Reranking |
| Containerization | Docker |
| CI/CD | GitHub Actions |
| Evaluation | Automated Labeled Query Evaluation |

---

## Project Structure

```text
lexora/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── agent.py
│   │   ├── main.py
│   │   └── retrieval.py
│   │
│   ├── ci/
│   │   └── eval-workflow.yml
│   │
│   ├── data/
│   │   └── circulars.json
│   │
│   ├── tests/
│   │   ├── eval_queries.json
│   │   └── test_eval.py
│   │
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   └── index.html
│
└── README.md
```

### Core Backend Components

| Component | Responsibility |
|---|---|
| `main.py` | FastAPI application and API endpoints |
| `retrieval.py` | Regulatory document retrieval and search pipeline |
| `agent.py` | LLM orchestration and agentic verification workflows |
| `circulars.json` | Regulatory document data |
| `eval_queries.json` | Labeled evaluation dataset |
| `test_eval.py` | Automated evaluation and testing |
| `eval-workflow.yml` | GitHub Actions evaluation workflow |
| `Dockerfile` | Backend containerization |

---

## Getting Started

### Prerequisites

- Python 3.10+
- pip
- PostgreSQL with pgvector support
- Supabase project
- Google Gemini API key
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/soumyadoshii/lexora.git
cd lexora
```

### 2. Navigate to the Backend

```bash
cd backend
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\Activate.ps1
```

Activate it on macOS/Linux:

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file in the backend directory and configure the credentials required by the application.

Typical configuration includes:

```env
GEMINI_API_KEY=your_gemini_api_key
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_api_key
DATABASE_URL=your_postgresql_connection_string
```

Use the exact variable names and configuration expected by the application code. Never commit API keys, database credentials, or other secrets to GitHub.

### 6. Run the Backend

```bash
uvicorn app.main:app --reload
```

The FastAPI development server will start locally.

API documentation is available through:

```text
http://127.0.0.1:8000/docs
```

### 7. Run with Docker

Build the backend image:

```bash
docker build -t lexora-backend ./backend
```

Run the container with the required environment configuration:

```bash
docker run -p 8000:8000 --env-file backend/.env lexora-backend
```

---

## Evaluation & Testing

Lexora incorporates an automated evaluation framework with 150+ labeled queries to assess its regulatory intelligence capabilities.

The evaluation suite is designed to examine:

- Retrieval of relevant regulatory evidence.
- Answer grounding against retrieved passages.
- Citation validity and source traceability.
- Correct abstention when evidence is insufficient.
- Reliability of the regulatory question-answering workflow.

Run the backend evaluation tests from the backend directory:

```bash
pytest -v
```

### Continuous Integration

GitHub Actions is integrated into the project to automate evaluation workflows.

The CI pipeline uses the evaluation dataset and backend tests to help detect regressions and maintain the reliability of the system.

---

## Engineering Highlights

- **Regulatory RAG Architecture:** Built a retrieval pipeline indexing 100+ RBI and SEBI circulars.
- **Hybrid Information Retrieval:** Combined semantic and keyword-based retrieval with reranking.
- **Agentic Verification:** Implemented three verification capabilities covering citation validation, unsupported-answer abstention, and regulatory document comparison.
- **Evidence-Based Generation:** Integrated Gemini API for context-grounded regulatory responses with source-level citations.
- **Vector Search Infrastructure:** Used PostgreSQL, Supabase, and pgvector for vector-based document retrieval.
- **Automated Evaluation:** Developed a labeled evaluation framework covering 150+ regulatory queries.
- **CI Integration:** Integrated automated evaluation workflows using GitHub Actions.
- **Containerization:** Packaged the backend using Docker for consistent deployment environments.

---

## Design Principles

### Grounded Over Generative
Regulatory answers should be supported by retrieved evidence rather than relying entirely on the language model's pretrained knowledge.

### Traceability
Users should be able to identify the regulatory sources supporting generated answers.

### Responsible Abstention
When the available evidence is insufficient, the system should avoid presenting unsupported conclusions.

### Modular Architecture
Document ingestion, retrieval, generation, verification, and evaluation are separated into distinct components to support maintainability and future improvements.

### Continuous Evaluation
Automated testing and labeled evaluation queries help monitor system behavior and identify regressions.

---

## Future Enhancements

Potential extensions to the platform include:

- Regulatory amendment and historical version tracking.
- Automated identification of changes between successive circulars.
- More granular regulatory topic classification.
- Advanced reranking and retrieval evaluation.
- Expanded support for additional financial regulators.
- Regulatory compliance checklists generated from cited provisions.
- Multi-document regulatory reasoning with cross-reference analysis.

---

## Disclaimer

Lexora is an educational and technical project for regulatory information retrieval and analysis. Its generated responses are intended to assist with understanding publicly available regulatory documents and should not be treated as legal, financial, or professional compliance advice.

Users should consult the original RBI and SEBI publications and qualified professionals before making regulatory or compliance decisions.
