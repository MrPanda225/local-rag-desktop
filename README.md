# Local RAG Desktop

A fully offline desktop application for querying your documents using a local AI model — no data leaves your machine.

---

## Overview

Local RAG Desktop combines a RAG pipeline with a local language model (via Ollama) to let you ask questions about your PDF documents without any internet connection. Built for privacy, speed, and clarity.

---

## What it does

- Loads and ingests PDF documents into a local vector database (Chroma)
- Retrieves relevant content based on your question
- Generates accurate answers using a local Ollama model (Mistral, Llama3, etc.)
- Runs entirely offline — no API calls, no data sent externally

---

## Architecture

```
RAG_TEST/
│
├── app/
│   ├── ingestion/        # PDF loading, chunking, embeddings, vector store
│   ├── rag/              # Retriever, generator, RAG pipeline
│   └── ui/               # Desktop interface
│
├── documents/            # Drop your PDFs here
├── db/                   # Chroma vector store
│
├── main_ingest.py        # Ingestion entry point
├── main.py               # Application entry point
├── requirements.txt
└── README.md
```

---

## Installation

**1. Clone the repository**

```bash
git clone https://github.com/MrPanda225/local-rag-desktop.git
cd RAG_TEST
```

**2. Create and activate a virtual environment**

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

---

## Ollama Setup

Download Ollama at [https://ollama.com/download](https://ollama.com/download), then pull the required models:

```bash
ollama pull mistral
ollama pull nomic-embed-text
```

---

## Usage

**Step 1 — Add your documents**

Place your PDF files in the `documents/` folder:

```
documents/your_file.pdf
```

**Step 2 — Run ingestion**

```bash
python main_ingest.py
```

This loads the PDF, splits it into chunks, generates embeddings, and stores them in the local vector database.

**Step 3 — Launch the application**

```bash
python main.py
```

You can now ask questions about your document directly from the interface.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.10+ |
| RAG Framework | LangChain |
| Vector Store | ChromaDB |
| LLM Runtime | Ollama (Mistral, Llama3) |
| Embeddings | Nomic Embed Text |
| PDF Processing | PyPDF |
| Desktop UI | CustomTkinter |

---

## Possible improvements

- PDF import directly from the UI
- Conversation history
- Dark / light mode toggle
- Model selection from the interface
- Chat bubble layout
- Response export
- REST API version (FastAPI)

---

## License

Free to use.
```
