from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List


class TextSplitter:
    """
    Découpe les documents en chunks de texte pour l'indexation.
    """

    def __init__(self, chunk_size: int = 800, overlap: int = 100):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap
        )

    def split(self, docs: List):
        """
        Retourne une liste de "documents" plus petits (chunks).
        """
        return self.splitter.split_documents(docs)
