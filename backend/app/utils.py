"""
utils.py — funciones auxiliares para streaming y manejo HTTP
"""

from typing import Dict, Generator, Any
import requests
from fastapi.responses import StreamingResponse


def stream_chunks(url: str, payload: Dict[str, Any]) -> StreamingResponse:
    """
    Envia un POST a Ollama /api/generate y devuelve la respuesta en streaming.
    Permite que el navegador o frontend reciba tokens en tiempo real.
    """
    def generate() -> Generator[bytes, None, None]:
        try:
            with requests.post(url, json=payload, stream=True, timeout=600) as r:
                r.raise_for_status()
                for line in r.iter_lines():
                    if line:
                        yield line + b"\n"
        except requests.exceptions.RequestException as e:
            yield f"Error: {str(e)}".encode("utf-8")

    return StreamingResponse(generate(), media_type="text/plain")