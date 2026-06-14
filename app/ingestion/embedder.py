from langchain_ollama import OllamaEmbeddings

from app.config import EMBEDDING_MODEL


class Embedder:
    """Fournit un objet d'embedding basé sur un modèle Ollama."""

    def __init__(self, model: str = EMBEDDING_MODEL):
        self.model_name = model

    def get(self) -> OllamaEmbeddings:
        return OllamaEmbeddings(model=self.model_name)