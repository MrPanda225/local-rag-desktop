from .document_loader import DocumentLoader
from .text_splitter import TextSplitter
from .embedder import Embedder
from .vector_store import VectorStore


def run_ingestion(doc_folder: str = "documents", db_folder: str = "db"):
    """
    Pipeline complet d'ingestion :
    - charge les documents
    - découpe en chunks
    - crée les embeddings
    - enregistre dans Chroma
    """
    print("➡️ Chargement des documents...")
    loader = DocumentLoader(doc_folder)
    docs = loader.load()

    print(f"✔ {len(docs)} pages chargées")

    splitter = TextSplitter()
    chunks = splitter.split(docs)
    print(f"✔ {len(chunks)} chunks générés")

    embedder = Embedder()
    embeddings = embedder.get()

    store = VectorStore(db_folder)
    print("➡️ Création de la base vectorielle...")
    store.create(chunks, embeddings)

    print("✅ Ingestion terminée et DB créée dans :", db_folder)
