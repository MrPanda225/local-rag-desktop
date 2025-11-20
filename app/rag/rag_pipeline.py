from .retriever import Retriever
from .generator import Generator


class RAGPipeline:
    """
    Pipeline Retrieval + Generation.
    """
    def __init__(self,
                 retrieval_top_k=4,
                 embedding_model="nomic-embed-text",
                 llm_model="mistral"):

        self.retriever = Retriever(
            top_k=retrieval_top_k,
            embedding_model=embedding_model
        )

        self.generator = Generator(model=llm_model)

    def ask(self, query: str) -> str:
        docs = self.retriever.search(query)
        context = "\n\n".join([doc.page_content for doc in docs])

        prompt = f"""
        Utilise uniquement ce contexte pour répondre :

        {context}

        QUESTION : {query}

        Répond clairement et précisément.
        """

        return self.generator.generate(prompt)
