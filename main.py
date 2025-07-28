from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pathlib import Path
from typing import List
import os

from extraction import extract_text
from pre_pipeline import preprocess_text
from rank_bm25 import BM25Okapi

def extract_snippet(doc_text: str, query_terms: List[str], window: int = 30) -> str:
    lowered_text = doc_text.lower()
    for term in query_terms:
        pos = lowered_text.find(term)
        if pos != -1:
            start = max(0, pos - window)
            end = min(len(doc_text), pos + window)
            return doc_text[start:end].replace('\n', ' ')
    return doc_text[:window * 2].replace('\n', ' ')  

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Constants
FOLDER = Path(r"c:\\Zaid\\Python_Practice\\Projects\\Document_IR_Backend\\docs")

# Request Model
class QueryRequest(BaseModel):
    query: str

# Response Model
class SearchResult(BaseModel):
    doc: str
    score: float
    snippet: str

# Load and preprocess documents on startup
@app.on_event("startup")
def load_documents():
    global bm25, doc_names, doc_texts
    doc_texts = []

    if not FOLDER.exists():
        raise FileNotFoundError(f"Docs folder does not exist: {FOLDER}")

    file_paths = [FOLDER / f for f in os.listdir(FOLDER) if (FOLDER / f).is_file()]
    doc_names = [f.name for f in file_paths]

    tokenized_docs = []
    for f in file_paths:
        try:
            raw = extract_text(f)
            doc_texts.append(raw)
            tokens = preprocess_text(raw)
            tokenized_docs.append(tokens)
        except Exception as e:
            print(f"[ERROR] Failed to process {f.name}: {e}")

    if not tokenized_docs:
        raise RuntimeError("No documents were processed.")

    bm25 = BM25Okapi(tokenized_docs)
    print("[INFO] Documents loaded and indexed.")

@app.post("/search", response_model=List[SearchResult])
def search_docs(request: QueryRequest):
    if not request.query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    query_tokens = preprocess_text(request.query)
    scores = bm25.get_scores(query_tokens)
    ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)

    results = []
    for idx, score in ranked:
        if score <= 0:
            continue
        original_text = doc_texts[idx]
        snippet = extract_snippet(original_text, query_tokens)
        results.append(SearchResult(
            doc=doc_names[idx],
            score=round(float(score), 4),
            snippet=snippet
        ))
    
    return results

@app.get("/download/{filename}")
def download_file(filename: str):
    file_path = FOLDER / filename

    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(path=str(file_path), filename=filename, media_type="application/octet-stream")

