# Lexora — Agentic Regulatory Intelligence (Demo)

A self-contained demo of the Lexora pipeline. It runs fully offline on **illustrative sample circulars** (not real RBI/SEBI text) — no API keys, database, or Docker needed.

## What it demonstrates
- **Hybrid retrieval**: BM25 keyword + char-n-gram semantic scoring, fused with Reciprocal Rank Fusion, then reranked by query-term coverage.
- **Source-level citations**: every answer sentence is tied to a circular ID and paragraph.
- **Citation validation**: each claim is checked verbatim against its cited paragraph.
- **Unsupported-answer abstention**: low evidence coverage → the system declines to answer.
- **Document comparison**: sentence-level diff (modified / added / removed) between two circulars.
- **Automated evaluation**: 27 labeled queries (21 answerable, 6 out-of-scope) run via pytest.

## Structure
```
README.md
backend/    FastAPI app, sample data, tests, Dockerfile, CI workflow template
frontend/   Static UI (served by the backend)
```

## Run
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
# open http://localhost:8000
```
Docker (from the project root): `docker build -f backend/Dockerfile -t lexora-demo . && docker run -p 8000:8000 lexora-demo`

## Evaluate
```bash
cd backend && pytest -q -s
```
CI: copy `backend/ci/eval-workflow.yml` to `.github/workflows/eval.yml` in your repo.

## API
`GET /api/documents` · `POST /api/ask {query, regulator?}` · `POST /api/compare {doc_a, doc_b}` · `GET /api/health`

## Moving to production
Replace the local components with: Gemini embeddings + generation, Supabase/PostgreSQL + pgvector storage, and a PDF ingestion pipeline for real circulars.
