from dataclasses import dataclass


@dataclass
class Config:
    # --- General ---
    DEBUG: bool = True

    # --- Ollama ---
    OLLAMA_HOST: str = "http://localhost:11434"  # donde corre ollama serve
    MODEL_DEFAULT: str = "phi4-mini:latest"

    # --- LLM Generation settings ---
    NUM_CTX: int = 128_000
    NUM_PREDICT: int = 256
    TEMPERATURE: float = 0.4

    # --- Paths ---
    DATA_DIR: str = "backend/data"
    DOCS_DIR: str = f"{DATA_DIR}/docs"
    CHROMA_DIR: str = f"{DATA_DIR}/chroma"


cfg = Config()