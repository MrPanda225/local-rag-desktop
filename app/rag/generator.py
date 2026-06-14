"""Module for LLM generation and query rewriting via Ollama."""
from langchain_ollama import OllamaLLM

from app.config import LLM_MODEL


class Generator:  # pylint: disable=too-few-public-methods
    """Handles generation with Ollama via OllamaLLM."""

    def __init__(self, model: str = LLM_MODEL):
        self.llm = OllamaLLM(model=model, temperature=0.0)

    def generate(self, prompt: str) -> str:
        """Generate a response from the LLM based on the prompt."""
        return self.llm.invoke(prompt)

    def rewrite_query(self, chat_history: list[tuple[str, str]], current_query: str) -> str:
        """Transform a follow-up question into a standalone question for retrieval."""
        user_questions = [q for q, _ in chat_history[-3:]]
        history_str = "\n".join(
            [f"Question précédente : {q}" for q in user_questions]
        )

        rewrite_prompt = (
            f"Tu es un expert en reformulation de requêtes pour un moteur de recherche.\n"
            f"{history_str}\n"
            f"Nouvelle question de suivi : {current_query}\n\n"
            f"Règle absolue : Reformule la nouvelle question pour qu'elle soit "
            f"compréhensible seule. Tu dois IMPÉRATIVEMENT inclure le sujet principal "
            f"des questions précédentes (ex: \"mensonge\"). Fais une phrase courte et "
            f"dense en mots-clés, sans verbe de requête comme \"Donne moi\" ou "
            f"\"Quels sont\".\n\n"
            f"Exemple : si la question est \"Donne m'en plus de détaille\" et le "
            f"sujet précédent est \"les signes du mensonge\", écris \"Détails et "
            f"explications sur les signes du mensonge\".\n\n"
            f"Requête reformulée :"
        )

        response = self.llm.invoke(rewrite_prompt).strip()

        for prefix in ["Requête reformulée :", "Question reformulée :", "Reformulation :"]:
            if response.lower().startswith(prefix.lower()):
                response = response.split(":", 1)[1].strip()

        return response
# Ligne vide finale ici
