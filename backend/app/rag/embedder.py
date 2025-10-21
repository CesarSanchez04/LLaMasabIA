import requests

# Modelo de embeddings en Ollama
EMBED_MODEL = "quentinz/bge-small-zh-v1.5:q8_0"
OLLAMA_URL = "http://localhost:11434/api/embeddings"

class OllamaEmbedder:
    def embed_docs(self, texts: list[str]) -> list[list[float]]:
        vectors = []
        for text in texts:
            payload = {"model": EMBED_MODEL, "input": text}
            r = requests.post(OLLAMA_URL, json=payload)
            r.raise_for_status()
            data = r.json()
            vectors.append(data["embedding"])
        return vectors

    def embed_query(self, text: str) -> list[float]:
        payload = {"model": EMBED_MODEL, "input": text}
        r = requests.post(OLLAMA_URL, json=payload)
        r.raise_for_status()
        return r.json()["embedding"]