from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma


class Retriever:
    """
    Récupère les chunks pertinents depuis la base vectorielle Chroma.
    """
    def __init__(self, db_folder="db", top_k=4, embedding_model="nomic-embed-text"):
        self.db_folder = db_folder
        self.top_k = top_k
        self.embedder = OllamaEmbeddings(model=embedding_model)

    def search(self, query: str):
        store = Chroma(
            persist_directory=self.db_folder,
            embedding_function=self.embedder,
        )
        return store.similarity_search(query, self.top_k)
