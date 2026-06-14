"""Main RAG Pipeline orchestrating retrieval, rewriting, and generation."""
from app.config import EMBEDDING_MODEL, LLM_MODEL
from app.ingestion.embedder import Embedder

from .generator import Generator  # pylint: disable=relative-beyond-top-level
from .retriever import Retriever  # pylint: disable=relative-beyond-top-level


class RAGPipeline:  # pylint: disable=too-few-public-methods
    """Pipeline Retrieval + Generation."""

    def __init__(
        self,
        retrieval_top_k: int = 10,
        embedding_model: str = EMBEDDING_MODEL,
        llm_model: str = LLM_MODEL
    ):
        embeddings = Embedder(model=embedding_model).get()
        self.retriever = Retriever(embeddings, top_k=retrieval_top_k)
        self.generator = Generator(model=llm_model)
        self.chat_history = []

    def ask(self, query: str) -> tuple[str, list]:
        """Process a user query: rewrite, retrieve, generate, and update history."""
        if self.chat_history:
            retrieval_query = self.generator.rewrite_query(self.chat_history, query)
            print(f"\n[DEBUG] Requête originale : {query}")
            print(f"[DEBUG] Requête reformulée pour retrieval : {retrieval_query}\n")
        else:
            retrieval_query = query

        docs = self.retriever.search(retrieval_query)

        context = ""
        for i, doc in enumerate(docs):
            context += f"[{i+1}] {doc.page_content}\n\n"

        history_str = ""
        for q, a in self.chat_history[-3:]:
            history_str += f"Utilisateur: {q}\nAssistant: {a}\n"

        # pylint: disable=line-too-long
        prompt = (
            f"<context>\n{context}\n</context>\n\n"
            f"Historique de la conversation:\n{history_str}\n\n"
            f"Règles strictes :\n"
            f"1. Réponds à la QUESTION en te basant UNIQUEMENT sur les informations présentes dans les balises <context> numérotées de [1] à [{len(docs)}].\n"
            f"2. Tu DOIS citer le numéro du chunk source entre crochets à la fin de chaque phrase ou élément de liste (ex: \"Le mensonge se voit aux mains [2].\").\n"
            f"3. N'invente JAMAIS de compte ou d'élément si tu ne peux pas le lier à un numéro de chunk. Liste uniquement les éléments que tu peux citer.\n"
            f"4. Si le <context> ne contient aucune information pour répondre, dis exactement : \"Les documents fournis ne contiennent pas cette information.\"\n"
            f"5. Ne fais JAMAIS appel à tes connaissances pré-entraînées.\n\n"
            f"QUESTION : {query}\n\n"
            f"Réponds clairement et précisément en respectant strictement les règles ci-dessus."
        )
        # pylint: enable=line-too-long

        response = self.generator.generate(prompt)
        self.chat_history.append((query, response))

        return response, docs
# Ligne vide finale ici