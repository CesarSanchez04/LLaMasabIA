# 🦙 LlamaSabia – Plataforma educativa offline con IA

**LlamaSabia** es una aplicación de escritorio desarrollada con **Electron + Python**, que busca reducir la brecha educativa entre universidades rurales y urbanas del Perú.  
Su objetivo es permitir que estudiantes de zonas con poca o nula conectividad puedan **alcanzar un nivel académico similar al de la UNI**, mediante **módulos de aprendizaje tipo sprint** acompañados de un **asistente virtual local con IA (LLM + RAG)**, totalmente **offline**.

---

## 🧩 Estructura general del proyecto

```bash
LlamaSabia/
├── README.md                         # Descripción general del proyecto
├── LICENSE                           # Licencia de uso
├── .gitignore                        # Archivos ignorados por Git
│
├── electron-app/                     # Interfaz de escritorio (Electron)
│   ├── package.json
│   ├── electron-builder.yml          # Configuración de build multiplataforma
│   ├── src/
│   │   ├── main/                     # Proceso principal de Electron
│   │   │   ├── main.ts               # Crea la ventana principal y levanta servicios
│   │   │   ├── ollama-daemon.ts      # Arranque del daemon Ollama (LLM embebido)
│   │   │   ├── backend-launcher.ts   # Ejecuta backend Python (FastAPI)
│   │   │   └── ipc.ts                # Comunicación segura Renderer <-> Main
│   │   ├── renderer/                 # Interfaz visual (React/Vue o HTML/JS)
│   │   │   ├── App.tsx
│   │   │   ├── ChatInterface.tsx     # Interacción con el asistente virtual
│   │   │   ├── ChapterSelector.tsx   # Selección de módulo o capítulo activo
│   │   │   └── styles/               # Archivos CSS o Tailwind
│   │   └── preload.ts
│   └── assets/
│       ├── logo.png
│       └── icons/
│
├── backend/                          # Backend local (Python + FastAPI)
│   ├── app/
│   │   ├── api.py                    # Endpoints principales (ask, health, chapter)
│   │   ├── rag/
│   │   │   ├── pipeline.py           # Flujo del RAG (retrieve → generate → verify)
│   │   │   ├── embedder.py           # Generación de embeddings locales
│   │   │   ├── store.py              # Gestión de bases ChromaDB/FAISS por capítulo
│   │   │   ├── sympy_checker.py      # Verificación simbólica (derivadas, límites)
│   │   │   └── context_builder.py    # Construcción del contexto del prompt
│   │   ├── config.py                 # Configuraciones globales (rutas, umbrales, modelo)
│   │   ├── guardrails.py             # Control de temas fuera de capítulo
│   │   └── utils.py
│   ├── requirements.txt              # Dependencias del backend
│   ├── venv/                         # Entorno virtual (opcional)
│   └── run_backend.sh                # Script para ejecutar el backend
│
├── engines/                          # Modelos y motor LLM embebido
│   ├── ollama/
│   │   ├── bin/                      # Binarios de Ollama o llama.cpp
│   │   ├── models/                   # Pesos del modelo LLM y embeddings
│   │   │   ├── llama3.2-8b.Q4_K_M.gguf
│   │   │   └── bge-small.gguf
│   │   └── run_ollama.sh             # Script de arranque del motor LLM
│   └── profiles/                     # Configuraciones CPU/GPU y cuantización
│
├── data/                             # Contenido académico y bases vectoriales
│   ├── vector_store/                 # Bases de datos vectoriales locales
│   │   ├── calculo/
│   │   │   ├── derivadas/
│   │   │   │   ├── index/
│   │   │   │   │   ├── chroma.sqlite
│   │   │   │   │   └── embeddings.parquet
│   │   │   │   └── manifest.json     # Versión, hash y fecha del capítulo
│   │   │   ├── limites/
│   │   │   │   └── index/...
│   │   │   └── regla_cadena/
│   │   │       └── index/...
│   ├── content/                      # Contenidos teóricos de cada sprint/módulo
│   │   ├── calculo/
│   │   │   ├── derivadas.md
│   │   │   ├── limites.md
│   │   │   └── regla_cadena.md
│   └── manifests/                    # Metadatos de corpus y modelos
│       ├── corpus_manifest.json
│       └── models_manifest.json
│
├── scripts/                          # Scripts auxiliares
│   ├── prepare_chapter.py            # Crea índices de embeddings por capítulo
│   ├── validate_env.sh               # Verifica dependencias locales
│   └── update_models.sh              # Importa o actualiza modelos sin Internet
│
└── docs/                             # Documentación y materiales complementarios
    ├── ARCHITECTURE.md               # Explicación técnica del sistema
    ├── INSTALLATION.md               # Guía de instalación offline
    ├── MODULE_CREATION_GUIDE.md      # Cómo crear nuevos módulos de aprendizaje
    ├── PITCH.md                      # Guion del video pitch
    ├── TEAM.md                       # Descripción del equipo y roles
    └── ROADMAP.md                    # Plan de desarrollo y expansión
