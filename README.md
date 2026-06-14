# Local RAG Desktop

A fully local desktop application for querying your documents with on-device AI, without sending data to the cloud.

Local RAG Desktop turns a collection of PDFs into a searchable knowledge base on your machine. The goal is simple: deliver reliable, cited, and fast answers while keeping both your documents and your conversations local.

## Why this project

Most document assistants promise accuracy, but often depend on external APIs or produce answers that are too generic. This project takes the opposite approach: it prioritizes privacy, traceability, and relevance.

It is built for use cases where data control is non-negotiable: internal documentation, research notes, domain-specific corpora, PDF reports, or personal knowledge bases.

## What the application delivers

- 100% local execution through Ollama.
- No API keys required.
- No data sent to third-party services.
- Answers grounded in passages actually retrieved from your documents.
- Natural follow-up questions supported through conversational context.
- An advanced RAG pipeline with hybrid search, reranking, and parent-child retrieval.

## How it works

The application follows a retrieval pipeline designed to reduce hallucinations and improve answer quality.

### 1. Document ingestion

PDF files placed in `documents/` are read, cleaned, and split into usable segments. The system then generates embeddings and stores the representations in a local vector database.

### 2. Hybrid search

When a question is asked, the engine combines two complementary approaches:

- Semantic search to retrieve passages close to the meaning of the query.
- BM25 lexical search to capture exact keywords, named entities, and specific expressions.

This combination improves recall without sacrificing precision.

### 3. Reranking

The first retrieved results are not equally useful. A reranker reevaluates the excerpts against the query and keeps only the most relevant passages for final generation.

### 4. Parent-child chunking

The system indexes small segments for precise retrieval, but sends a larger text block to the model when generating an answer. This preserves context without weakening relevance.

### 5. Query rewriting

For follow-up questions, a rewriting step converts an implicit request into a standalone query. This helps the system resolve contextual references and maintain a natural conversation flow.

### 6. Constrained generation

The generation model answers only from the supplied context. If the information does not appear in the retrieved documents, the application must say so explicitly instead of inventing an answer.

## Features

- Source-grounded answers based on uploaded documents.
- Conversational memory for follow-up questions.
- Fully offline execution on a local machine.
- Desktop interface built with CustomTkinter.
- Local vector storage powered by ChromaDB.
- An advanced RAG pipeline that is ready to extend.

## Project architecture

```text
local-rag-desktop/
│
├── app/
│   ├── config.py              # Model configuration (LLM and embeddings)
│   ├── ingestion/
│   │   ├── document_loader.py # PDF extraction with PyMuPDF
│   │   ├── text_splitter.py   # Parent-child chunking logic
│   │   ├── embedder.py        # Embedding generation through Ollama
│   │   ├── vector_store.py    # ChromaDB management
│   │   └── ingest.py          # Ingestion pipeline
│   │
│   ├── rag/
│   │   ├── retriever.py       # Hybrid search, reranking, and parent expansion
│   │   ├── generator.py       # Generation and query rewriting
│   │   └── rag_pipeline.py    # Orchestration and anti-hallucination guardrails
│   │
│   └── ui/
│       └── desktop.py         # CustomTkinter desktop interface
│
├── documents/                 # Drop your PDFs here
├── db/                        # Local vector database generated automatically
│
├── main_ingest.py             # Step 1: ingest documents
├── main.py                    # Step 2: launch the application
├── requirements.txt
└── README.md
```

## Tech stack

| Layer | Technology | Role |
|-------|------------|------|
| Language | Python 3.10+ | Application logic |
| RAG orchestration | LangChain | Pipeline construction |
| Vector database | ChromaDB | Vector storage and retrieval |
| Lexical search | BM25 (`rank-bm25`) | Exact keyword matching |
| Reranking | FlashRank | Sorting passages by relevance |
| LLM runtime | Ollama | Local model execution |
| Generation model | Qwen 2.5 7B | Answer generation and query rewriting |
| Embedding model | Nomic Embed Text | Text vectorization |
| PDF processing | PyMuPDF | Text extraction |
| Interface | CustomTkinter | Desktop application |

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/MrPanda225/local-rag-desktop.git
cd local-rag-desktop
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the environment

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

## Ollama setup

Install [Ollama](https://ollama.com/download), then download the required models.

```bash
ollama pull qwen2.5:7b-instruct-q4_K_M
ollama pull nomic-embed-text
```

## Quick start

### 1. Add documents

Place your PDF files in the `documents/` folder.

### 2. Run ingestion

```bash
python main_ingest.py
```

This step extracts text, builds parent-child chunks, computes embeddings, and fills the local `db/` database.

### 3. Launch the application

```bash
python main.py
```

You can then ask a question, request clarification, or continue with follow-up prompts. Answers are grounded strictly in passages retrieved from your documents.

## Use cases

- Query a domain-specific PDF collection without relying on a cloud service.
- Explore local technical documentation with cited answers.
- Build a private document assistant for research or internal teams.
- Validate information quickly inside a specialized corpus.

## Roadmap

- [ ] Add dark mode and light mode.
- [ ] Improve conversation rendering with chat bubbles.
- [ ] Allow PDF import directly from the interface.
- [ ] Add streaming responses.
- [ ] Integrate an OCR pipeline for scanned PDFs.
- [ ] Expose a FastAPI wrapper for web integration.
