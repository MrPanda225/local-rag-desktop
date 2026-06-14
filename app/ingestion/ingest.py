"""Main ingestion pipeline script."""
from .document_loader import DocumentLoader
from .embedder import Embedder
from .text_splitter import ParentChildSplitter
from .vector_store import VectorStore


def run_ingestion(doc_folder: str = "documents", db_folder: str = "db"):
    """
    Complete ingestion pipeline:
    - Loads documents
    - Splits into Parent/Child chunks
    - Creates embeddings
    - Saves to ChromaDB
    """
    print("Chargement des documents...")
    loader = DocumentLoader(doc_folder)
    docs = loader.load()
    print(f"✔ {len(docs)} pages chargées")

    splitter = ParentChildSplitter()
    chunks = splitter.split(docs)
    print(f"✔ {len(chunks)} chunks générés (Parents + Enfants)")

    doc_ids = [c.metadata["doc_id"] for c in chunks]

    embedder = Embedder()
    embeddings = embedder.get()

    store = VectorStore(db_folder)
    print("Création de la base vectorielle...")
    store.create(chunks, embeddings, doc_ids=doc_ids)

    print("✔ Ingestion terminée et DB créée dans :", db_folder)