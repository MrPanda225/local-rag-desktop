from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List


class TextSplitter:
    """
    Découpe les documents en chunks de texte pour l'indexation.
    Optimisé pour préserver le contexte des paragraphes et des listes.
    """

    def __init__(self, chunk_size: int = 1000, overlap: int = 200):
        # Séparateurs hiérarchiques pour un découpage intelligent
        separators = [
            "\n\n",  # 1. Priorité : coupure entre les paragraphes
            "\n",    # 2. Coupure entre les lignes
            ". ",    # 3. Coupure entre les phrases
            " ",     # 4. Coupure entre les mots
            ""       # 5. Dernier recours : coupure caractère par caractère
        ]
        
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap,
            separators=separators,
            length_function=len,
            is_separator_regex=False,
        )

    def split(self, docs: List):
        """
        Retourne une liste de "documents" plus petits (chunks).
        """
        return self.splitter.split_documents(docs)