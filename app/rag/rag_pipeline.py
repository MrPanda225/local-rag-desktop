from app.config import EMBEDDING_MODEL, LLM_MODEL
from app.ingestion.embedder import Embedder

from .retriever import Retriever
from .generator import Generator


class RAGPipeline:
    """Pipeline Retrieval + Generation."""

    def __init__(self,
                 retrieval_top_k: int = 10,
                 embedding_model: str = EMBEDDING_MODEL,
                 llm_model: str = LLM_MODEL):

        embeddings = Embedder(model=embedding_model).get()
        self.retriever = Retriever(embeddings, top_k=retrieval_top_k)
        self.generator = Generator(model=llm_model)

        self.chat_history = []

    def ask(self, query: str) -> tuple[str, list]:
        
        # --- REFORMULATION PAR LLM ---
        if self.chat_history:
            retrieval_query = self.generator.rewrite_query(self.chat_history, query)
            # DEBUG : Affiche la requête reformulée dans la console pour comprendre le retrieval
            print(f"\n[DEBUG] Requête originale : {query}")
            print(f"[DEBUG] Requête reformulée pour retrieval : {retrieval_query}\n")
        else:
            retrieval_query = query

        # Recherche (Hybride + Rerank) avec la requête reformulée
        docs = self.retriever.search(retrieval_query)
        
        # --- Contexte numéroté ---
        context = ""
        for i, doc in enumerate(docs):
            context += f"[{i+1}] {doc.page_content}\n\n"

        history_str = ""
        for q, a in self.chat_history[-3:]:
            history_str += f"Utilisateur: {q}\nAssistant: {a}\n"

        # --- PROMPT ---
        prompt = f"""<context>
{context}
</context>

Historique de la conversation:
{history_str}

Règles strictes :
1. Réponds à la QUESTION en te basant UNIQUEMENT sur les informations présentes dans les balises <context> numérotées de [1] à [{len(docs)}].
2. Tu DOIS citer le numéro du chunk source entre crochets à la fin de chaque phrase ou élément de liste (ex: "Le mensonge se voit aux mains [2].").
3. N'invente JAMAIS de compte ou d'élément si tu ne peux pas le lier à un numéro de chunk. Liste uniquement les éléments que tu peux citer.
4. Si le <context> ne contient aucune information pour répondre, dis exactement : "Les documents fournis ne contiennent pas cette information."
5. Ne fais JAMAIS appel à tes connaissances pré-entraînées.

QUESTION : {query}

Réponds clairement et précisément en respectant strictement les règles ci-dessus."""

        # Génération de la réponse finale
        response = self.generator.generate(prompt)

        # Mise à jour de l'historique avec la question ORIGINALE
        self.chat_history.append((query, response))

        return response, docs