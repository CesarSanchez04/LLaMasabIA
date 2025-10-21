from typing import List, Dict

TEMPLATE = """Eres LlamaSabia. Responde en español de forma clara y concisa.
Usa SOLO la información del CONTEXTO. Si no está, di: "No está en el contexto".
Cita la(s) fuente(s) con [id].

PREGUNTA:
{question}

CONTEXTO:
{contexts}
"""

def build_context(query: str, docs: List[Dict]) -> str:
    blocks = []
    for d in docs:
        tag = d.get("id", "doc")
        txt = (d.get("text") or "").replace("\n", " ")
        blocks.append(f"[{tag}] {txt}")
    return TEMPLATE.format(question=query, contexts="\n\n".join(blocks))