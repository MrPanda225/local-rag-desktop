import shutil
from pathlib import Path
from typing import List

from langchain_community.vectorstores import Chroma


class VectorStore:
    """Gère le store vectoriel Chroma persisté sur disque."""

    def __init__(self, persist_dir: str = "db"):
        self.persist_dir = persist_dir

    def create(self, documents: List, embeddings) -> None:
        """
        Remplace le store vectoriel à persist_dir par les documents fournis.

        Supprime d'abord le store existant à persist_dir : rappeler cette
        méthode avec des documents mis à jour ne duplique donc pas les
        entrées précédentes.

        Lève:
            OSError: si le dossier du store existant ne peut pas être
                supprimé (par ex. l'app desktop tourne et le garde ouvert).
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
            persist_directory=self.persist_dir,
        )