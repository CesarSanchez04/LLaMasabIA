"""
guardrails.py — filtros y validaciones ligeras antes de enviar el prompt al modelo
"""

from typing import Dict, Any


def apply_guardrails(prompt_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sanitiza y valida el prompt antes de enviarlo al modelo Ollama.
    Puede servir para evitar prompts vacíos, inyecciones o entradas malformadas.
    """
    text = prompt_data.get("prompt", "").strip()

    if not text:
        prompt_data["prompt"] = "Por favor, proporciona una pregunta válida."
        return prompt_data

    # Reglas básicas de seguridad (puedes ampliar con regex o listas negras)
    banned = ["shutdown", "delete", "format", "sudo", "rm -rf"]
    if any(bad in text.lower() for bad in banned):
        prompt_data["prompt"] = "⚠️ Comando bloqueado por seguridad."
        return prompt_data

    return prompt_data