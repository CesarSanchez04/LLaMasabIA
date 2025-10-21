from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from .config import cfg
from .guardrails import apply_guardrails
from .utils import stream_chunks
from .rag.pipeline import ingest_path, retrieve
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="LLaMasabIA API", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "ok", "service": "LLaMasabIA API"}

@app.get("/health")
def health():
    return {"ok": True}

class IngestIn(BaseModel):
    path: str
    namespace: str = "general"

class AskIn(BaseModel):
    prompt: str
    model: str = "llamasabia"  # o "phi4-mini" si no creaste Modelfile
    stream: bool = False

class AskRAGIn(BaseModel):
    prompt: str
    model: str = "llamasabia"
    stream: bool = False
    top_k: int = 4
    namespace: str = "general"

@app.post("/ingest")
def ingest(body: IngestIn):
    try:
        res = ingest_path(body.path, namespace=body.namespace)
        return {"status": "ok", **res}
    except Exception as e:
        raise HTTPException(400, f"Ingest error: {e}")

@app.post("/ask_rag")
def ask_rag(body: AskRAGIn):
    ctx, hits = retrieve(body.prompt, top_k=body.top_k, namespace=body.namespace)
    payload = {
        "model": body.model,
        "prompt": ctx,
        "stream": body.stream,
        "options": {
            "num_ctx": cfg.NUM_CTX,
            "num_predict": cfg.NUM_PREDICT,
            "temperature": cfg.TEMPERATURE
        }
    }
    if body.stream:
        return stream_chunks(f"{cfg.OLLAMA_HOST}/api/generate", payload)
    try:
        r = requests.post(f"{cfg.OLLAMA_HOST}/api/generate", json=payload, timeout=120)
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Ollama request failed: {e}")
    return {"response": data.get("response", ""), "hits": hits}