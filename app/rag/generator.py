from langchain_ollama import OllamaLLM


class Generator:
    """
    Gère la génération avec Ollama en utilisant la nouvelle API OllamaLLM.
    """
    def __init__(self, model="mistral"):
        self.llm = OllamaLLM(model=model)

    def generate(self, prompt: str) -> str:
        return self.llm.invoke(prompt)
