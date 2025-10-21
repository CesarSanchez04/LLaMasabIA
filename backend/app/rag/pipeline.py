from typing import Tuple, List, Dict, Optional
from pathlib import Path
from uuid import uuid4
from .loaders import load_and_chunk
from ..store import get_store
from .context_builder import build_context

def ingest_path(path: str, namespace: str = "general") -> Dict[str, str]:
    store = get_store()
    chunks = load_and_chunk(path)
    fname = Path(path).name
    docs = []
    for i, ch in enumerate(chunks):
        docs.append({
            "id": f"{fname}-{i}-{uuid4().hex[:8]}",
            "text": ch,
            "metadata": {"source": fname, "ns": namespace, "i": i}
        })
    store.upsert(docs)
    return {"file": fname, "chunks": str(len(chunks)), "namespace": namespace}

def retrieve(query: str, top_k: int = 4, namespace: Optional[str] = None) -> Tuple[str, List[Dict]]:
    store = get_store()
    where = {"ns": namespace} if namespace else None
    hits = store.search(query, top_k=top_k, where=where)
    ctx = build_context(query, hits)
    return ctx, hits