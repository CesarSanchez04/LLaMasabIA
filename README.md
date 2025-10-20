LlamaSabia/
├── README.md
├── LICENSE
├── .gitignore
│
├── electron-app/                     # Interfaz de escritorio (Electron)
│   ├── package.json
│   ├── electron-builder.yml           # Configuración de build multiplataforma
│   ├── src/
│   │   ├── main/                      # Proceso principal (manejo de ventanas y servicios)
│   │   │   ├── main.ts
│   │   │   ├── ollama-daemon.ts       # Arranque del daemon Ollama
│   │   │   ├── backend-launcher.ts    # Ejecuta backend Python (FastAPI)
│   │   │   └── ipc.ts                 # Comunicación segura Renderer <-> Main
│   │   ├── renderer/                  # Interfaz visual (React/Vue/HTML)
│   │   │   ├── App.tsx
│   │   │   ├── ChapterSelector.tsx
│   │   │   ├── ChatInterface.tsx
│   │   │   └── styles/
│   │   └── preload.ts
│   └── assets/
│       ├── logo.png
│       └── icons/
│
├── backend/                          # Backend local (Python)
│   ├── app/
│   │   ├── api.py                    # Endpoints /ask, /health, /chapter
│   │   ├── rag/
│   │   │   ├── pipeline.py           # Flujo RAG (retrieve → generate)
│   │   │   ├── embedder.py           # Generación de embeddings locales
│   │   │   ├── store.py              # Gestión ChromaDB/FAISS por capítulo
│   │   │   └── sympy_checker.py      # Verificación de resultados matemáticos
│   │   ├── config.py                 # Config general (rutas, umbrales)
│   │   ├── guardrails.py             # Control de temas fuera de capítulo
│   │   └── utils.py
│   ├── venv/                         # Entorno virtual (opcional para el build)
│   ├── requirements.txt
│   └── run_backend.sh                # Script para ejecutar el backend
│
├── engines/                          # LLM y embeddings locales
│   ├── ollama/
│   │   ├── bin/                      # Binarios Ollama o llama.cpp
│   │   ├── models/
│   │   │   ├── llama3.2-8b.Q4_K_M.gguf
│   │   │   └── bge-small.gguf
│   │   └── run_ollama.sh             # Arranque del motor LLM
│   └── profiles/                     # Config de CPU/GPU y cuantización
│
├── data/
│   ├── vector_store/                 # BD vectoriales locales (por módulo)
│   │   ├── calculo/
│   │   │   ├── derivadas/
│   │   │   │   ├── index/
│   │   │   │   │   ├── chroma.sqlite
│   │   │   │   │   └── embeddings.parquet
│   │   │   │   └── manifest.json     # Versión, hash, fecha
│   │   │   ├── limites/
│   │   │   │   └── index/...
│   │   │   └── regla_cadena/
│   │   │       └── index/...
│   ├── content/                      # Textos base de los módulos
│   │   ├── calculo/
│   │   │   ├── derivadas.md
│   │   │   ├── limites.md
│   │   │   └── regla_cadena.md
│   └── manifests/
│       ├── corpus_manifest.json
│       └── models_manifest.json
│
├── scripts/                          # Herramientas y tareas administrativas
│   ├── prepare_chapter.py            # Crea índices de embeddings por capítulo
│   ├── validate_env.sh               # Verifica dependencias locales
│   └── update_models.sh              # Importa modelos desde assets sin Internet
│
└── docs/                             # Documentación y materiales
    ├── ARCHITECTURE.md               # Explicación técnica
    ├── INSTALLATION.md               # Instrucciones de instalación offline
    ├── MODULE_CREATION_GUIDE.md      # Cómo crear nuevos sprints/módulos
    ├── PITCH.md                      # Guion del video pitch
    ├── TEAM.md                       # Descripción del equipo y roles
    └── ROADMAP.md                    # Plan de desarrollo
