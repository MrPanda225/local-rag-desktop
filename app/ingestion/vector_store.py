from langchain_community.vectorstores import Chroma
from typing import List


class VectorStore:
    """
    Gère la création de la base vectorielle dans Chroma.
    """

    def __init__(self, persist_dir: str = "db"):
        self.persist_dir = persist_dir

    def create(self, documents: List, embeddings):
        """
        Crée / remplace la base vectorielle à partir des documents chunkés.
        """
        Chroma.from_documents(
            documents=documents,
            embedding=embeddings,
            persist_directory=self.persist_dir
        )
