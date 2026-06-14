"""Module for loading PDF documents from a directory."""
from pathlib import Path
from typing import List

from langchain_community.document_loaders import PyMuPDFLoader


class DocumentLoader:  # pylint: disable=too-few-public-methods
    """Loads all PDF files from a specified directory into LangChain Documents."""

    def __init__(self, folder: str):
        self.folder = Path(folder)

    def load(self) -> List:
        """Load and return a list of documents from all PDFs in the folder."""
        if not self.folder.exists():
            raise FileNotFoundError(f"Dossier introuvable : {self.folder}")

        documents = []
        for file in self.folder.iterdir():
            if file.suffix.lower() == ".pdf":
                loader = PyMuPDFLoader(str(file))
                docs = loader.load()
                documents.extend(docs)

        if not documents:
            raise ValueError(f"Aucun PDF trouvé dans {self.folder}")

        return documents
# Ligne vide finale ici