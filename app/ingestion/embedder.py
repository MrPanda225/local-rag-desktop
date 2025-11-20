from langchain_ollama import OllamaEmbeddings

class Embedder:
    """
    Fournit un objet d'embedding basé sur un modèle Ollama.
    """

    def __init__(self, model: str = "nomic-embed-text"):
        self.model_name = model

    def get(self) -> OllamaEmbeddings:
        return OllamaEmbeddings(model=self.model_name)
