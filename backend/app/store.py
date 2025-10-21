from typing import Optional, List, Dict, Any
from pathlib import Path
import chromadb
from chromadb.config import Settings
from backend.app.rag.embedder import OllamaEmbedder

DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "chroma"
COLLECTION = "llamasabia_docs"


class VectorStore:
    def __init__(self, persist_dir: Optional[str] = None) -> None:
        self.persist_dir = str(persist_dir or DATA_DIR)
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        self.client = chromadb.PersistentClient(
            path=self.persist_dir,
            settings=Settings(allow_reset=True)
        )
        # espacio de similitud: cosine
        self.col = self.client.get_or_create_collection(
            name=COLLECTION,
            metadata={"hnsw:space": "cosine"}
        )
        self.embedder = OllamaEmbedder()

    def upsert(self, docs: List[Dict[str, Any]]) -> None:
        """
        docs: [{ 'id': str, 'text': str, 'metadata': dict }]
        """
        if not docs:
            return
        ids = [d["id"] for d in docs]
        texts = [d["text"] for d in docs]
        metas = [d.get("metadata", {}) for d in docs]
        embs = self.embedder.embed_docs(texts)
        self.col.upsert(ids=ids, documents=texts, embeddings=embs, metadatas=metas)

    def search(self, query: str, top_k: int = 4, where: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        q_emb = self.embedder.embed_query(query)
        res = self.col.query(
            query_embeddings=[q_emb],
            n_results=top_k,
            where=where
        )
        hits: List[Dict[str, Any]] = []
        if not res or not res.get("documents"):
            return hits
        docs = res["documents"][0]
        ids = res["ids"][0]
        dists = res.get("distances", [[None]])[0]
        metas = res.get("metadatas", [[{}]])[0]
        for i, txt in enumerate(docs):
            hits.append({"id": ids[i], "text": txt, "score": dists[i], "metadata": metas[i]})
        return hits


# singleton sencillo
_vs: Optional[VectorStore] = None
def get_store() -> VectorStore:
    global _vs
    if _vs is None:
        _vs = VectorStore()
    return _vs