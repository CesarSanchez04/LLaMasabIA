from typing import List
from pathlib import Path
from pypdf import PdfReader

def load_text_file(path: str) -> str:
    return Path(path).read_text(encoding="utf-8", errors="ignore")

def load_pdf(path: str) -> str:
    reader = PdfReader(path)
    pages = [(p.extract_text() or "") for p in reader.pages]
    return "\n\n".join(pages)

def chunk_text(text: str, chunk_size: int = 800, overlap: int = 120) -> List[str]:
    chunks: List[str] = []
    start = 0
    n = len(text)
    while start < n:
        end = min(start + chunk_size, n)
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start = end - overlap
        if start < 0:
            start = 0
        if start >= n:
            break
    return chunks

def load_and_chunk(path: str, chunk_size: int = 800, overlap: int = 120) -> List[str]:
    p = Path(path)
    if p.suffix.lower() == ".pdf":
        txt = load_pdf(path)
    else:
        txt = load_text_file(path)
    return chunk_text(txt, chunk_size=chunk_size, overlap=overlap)