# Local RAG Desktop

A fully offline desktop application for querying your documents using a local AI. No data ever leaves your machine.

---

## How It Works

Before diving into the tech, here is how the AI reads and answers your documents, step by step:

### 1. The Open-Book Exam (RAG)
Instead of letting the AI guess the answer from its memory (which causes hallucinations), we use **RAG (Retrieval-Augmented Generation)**. Think of it as an open-book exam: we first find the exact paragraph in your document, then we ask the AI to read only that paragraph to write the answer.

### 2. The Librarian & The Detective (Hybrid Search)
When you search for a document, you need two things:
*   **Semantic Search (The Librarian):** Understands the *meaning* of your question ("signs of lying") even if the text says "deception indicators".
*   **BM25 Keyword Search (The Detective):** Finds exact words ("Tony Blair") that the Librarian might miss.
We combine both to find the best possible excerpts.

### 3. The Bouncer (Reranking)
Our search retrieves 20+ excerpts. Some are great, some are irrelevant. The **Reranker** acts like a bouncer: it reads all of them specifically against your question and keeps only the top 4 most relevant ones. Quality over quantity.

### 4. Reading the Index, then the Chapter (Parent-Child Chunking)
If we only feed the AI a random sentence, it misses the context. If we feed it whole pages, it gets lost. 
Our solution: We index **small chunks** (Child) for precise searching, but when we find a match, we give the AI the **whole paragraph** (Parent) it belongs to. It’s like finding a word in the index, then reading the full chapter.

### 5. The Translator (Query Rewriting)
If you ask *"What about its implications?"* after a question about lying, the AI might get confused. Our system uses a fast LLM to rewrite your follow-up into a standalone question: *"What are the implications of the signs of lying?"* before searching. 

### 6. The Fact-Checker (Anti-Hallucination)
The AI is strictly forbidden from using its own memory. If the answer isn't in the provided text, it must say *"The documents do not contain this information."* It must also cite its sources `[1]` for every claim it makes.

---

## Features

-   **100% Offline & Private:** Runs entirely on Ollama. No API keys, no data sent to the cloud.
-   **Conversational Memory:** Ask follow-up questions naturally; the system understands the context.
-   **Sourced Answers:** Every response shows the exact document chunks used to generate it.
-   **Advanced RAG Pipeline:** Hybrid Search, Flashrank Reranking, Parent-Child retrieval, and LLM Query Rewriting out of the box.

---

## Architecture

```text
local-rag-desktop/
│
├── app/
│   ├── config.py              # Models configuration (LLM & Embeddings)
│   ├── ingestion/
│   │   ├── document_loader.py # PDF extraction (PyMuPDF)
│   │   ├── text_splitter.py   # Parent-Child chunking logic
│   │   ├── embedder.py        # Ollama embeddings
│   │   ├── vector_store.py    # ChromaDB management
│   │   └── ingest.py          # Ingestion pipeline
│   │
│   ├── rag/
│   │   ├── retriever.py       # Hybrid Search + Reranking + Parent expansion
│   │   ├── generator.py       # LLM generation & Query Rewriting
│   │   └── rag_pipeline.py    # Orchestrator with anti-hallucination prompts
│   │
│   └── ui/
│       └── desktop.py         # CustomTkinter GUI
│
├── documents/                 # Drop your PDFs here
├── db/                        # Local Chroma vector store (auto-generated)
│
├── main_ingest.py             # Step 1: Ingest documents
├── main.py                    # Step 2: Launch the app
├── requirements.txt
└── README.md
```


## Installation

**1. Clone the repository**

```bash
git clone https://github.com/MrPanda225/local-rag-desktop.git
cd local-rag-desktop
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

Download and install [Ollama](https://ollama.com/download), then pull the required models:

```bash
# The fast, smart model for generation and query rewriting
ollama pull qwen2.5:7b-instruct-q4_K_M

# The model that transforms text into vectors (meaning)
ollama pull nomic-embed-text
```

---

## Usage

**Step 1 — Add your documents**

Place your PDF files in the `documents/` folder.

**Step 2 — Run ingestion**

```bash
python main_ingest.py
```
*This extracts the text, cuts it into Parent/Child chunks, generates embeddings, and stores everything in the local `db/` folder.*

**Step 3 — Launch the application**

```bash
python main.py
```

Ask questions, request details, and follow up naturally. The AI will answer based strictly on your documents and show you its sources.

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Language | Python 3.10+ | Core logic |
| RAG Framework | LangChain | Pipeline orchestration |
| Vector Store | ChromaDB | Storing & searching embeddings |
| Sparse Search | BM25 (rank-bm25) | Exact keyword matching |
| Reranking | FlashRank | Sorting search results by relevance |
| LLM Runtime | Ollama | 100% local AI inference |
| LLM Model | Qwen 2.5 7B | Answer generation & Query rewriting |
| Embeddings | Nomic Embed Text | Transforming text into vectors |
| PDF Processing | PyMuPDF | High-quality text extraction |
| Desktop UI | CustomTkinter | Modern desktop interface |

---

## Possible Improvements

- [ ] UI: Dark / light mode toggle
- [ ] UI: Chat bubble layout instead of raw text
- [ ] UI: PDF import button directly from the interface
- [ ] Core: Streaming responses (token by token)
- [ ] Core: OCR correction pipeline for scanned PDFs
- [ ] API: FastAPI wrapper for web integration
```