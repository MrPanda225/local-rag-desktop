"""Module for initializing the Ollama embedding model."""
from langchain_ollama import OllamaEmbeddings

from app.config import EMBEDDING_MODEL


class Embedder:  # pylint: disable=too-few-public-methods
    """Provides an embedding object based on an Ollama model."""

    def __init__(self, model: str = EMBEDDING_MODEL):
        self.model_name = model

    def get(self) -> OllamaEmbeddings:
        """Return the configured OllamaEmbeddings instance."""
        return OllamaEmbeddings(model=self.model_name)