"""Module for managing the ChromaDB vector store."""
import shutil
from pathlib import Path
from typing import List, Optional

from langchain_community.vectorstores import Chroma


class VectorStore:  # pylint: disable=too-few-public-methods
    """Manages the persistent Chroma vector store."""

    def __init__(self, persist_dir: str = "db"):
        self.persist_dir = persist_dir

    def create(self, documents: List, embeddings, doc_ids: Optional[List[str]] = None) -> None:
        """
        Replace the vector store at persist_dir with the provided documents.
        Raises OSError if the existing directory cannot be removed.
        """
        store_path = Path(self.persist_dir)
        if store_path.exists():
            try:
                shutil.rmtree(store_path)
            except OSError as exc:
                raise OSError(
                    f"Impossible de supprimer le store existant à {store_path}. "
                    "Ferme l'app desktop si elle tourne, puis réessaie."
                ) from exc

        Chroma.from_documents(
            documents=documents,
            embedding=embeddings,
            ids=doc_ids,
            persist_directory=self.persist_dir,
        )