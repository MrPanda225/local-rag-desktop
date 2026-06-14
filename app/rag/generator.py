from langchain_ollama import OllamaLLM
from app.config import LLM_MODEL

class Generator:
    """Gère la génération avec Ollama via OllamaLLM."""

    def __init__(self, model: str = LLM_MODEL):
        self.llm = OllamaLLM(model=model, temperature=0.0)

    def generate(self, prompt: str) -> str:
        return self.llm.invoke(prompt)

    def rewrite_query(self, chat_history: list[tuple[str, str]], current_query: str) -> str:
        """Transforme une question de suivi en question autonome pour le retrieval."""
        
        # On ne garde que les questions de l'utilisateur pour éviter 
        # que le LLM ne soit pollué par ses propres réponses ("Je ne sais pas")
        user_questions = [q for q, a in chat_history[-3:]]
        history_str = "\n".join([f"Question précédente : {q}" for q in user_questions])

        rewrite_prompt = f"""Tu es un expert en reformulation de requêtes pour un moteur de recherche.
{history_str}
Nouvelle question de suivi : {current_query}

Règle absolue : Reformule la nouvelle question pour qu'elle soit compréhensible seule. Tu dois IMPÉRATIVEMENT inclure le sujet principal des questions précédentes (ex: "mensonge"). Fais une phrase courte et dense en mots-clés, sans verbe de requête comme "Donne moi" ou "Quels sont". 

Exemple : si la question est "Donne m'en plus de détaille" et le sujet précédent est "les signes du mensonge", écris "Détails et explications sur les signes du mensonge".

Requête reformulée :"""

        response = self.llm.invoke(rewrite_prompt).strip()
        
        # Nettoyage des préfixes potentiels du LLM
        for prefix in ["Requête reformulée :", "Question reformulée :", "Reformulation :"]:
            if response.lower().startswith(prefix.lower()):
                response = response.split(":", 1)[1].strip()
                    
        return response