import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
from .agent import ask, compare, get_index

app = FastAPI(title="Lexora Demo", version="0.1.0")

class AskReq(BaseModel):
    query: str
    regulator: Optional[str] = None

class CompareReq(BaseModel):
    doc_a: str
    doc_b: str

@app.get("/api/health")
def health(): return {"status": "ok", "documents": len(get_index().docs)}

@app.get("/api/documents")
def documents():
    return get_index().docs

@app.post("/api/ask")
def ask_ep(r: AskReq):
    if not r.query.strip(): raise HTTPException(400, "Empty query")
    return ask(r.query, r.regulator)

@app.post("/api/compare")
def compare_ep(r: CompareReq):
    try: return compare(r.doc_a, r.doc_b)
    except KeyError: raise HTTPException(404, "Unknown document id")

FRONTEND = os.environ.get("FRONTEND_DIR", os.path.join(os.path.dirname(__file__), "..", "..", "frontend"))
if os.path.isdir(FRONTEND):
    app.mount("/", StaticFiles(directory=FRONTEND, html=True), name="frontend")
