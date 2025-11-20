from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path
from typing import List


class DocumentLoader:
    """
    Charge tous les fichiers PDF d'un dossier et renvoie une liste de documents LangChain.
    """

    def __init__(self, folder: str):
        self.folder = Path(folder)

    def load(self) -> List:
        if not self.folder.exists():
            raise FileNotFoundError(f"Dossier introuvable : {self.folder}")

        documents = []
        for file in self.folder.iterdir():
            if file.suffix.lower() == ".pdf":
                loader = PyPDFLoader(str(file))
                docs = loader.load()
                documents.extend(docs)

        if not documents:
            raise ValueError(f"Aucun PDF trouvé dans {self.folder}")

        return documents
