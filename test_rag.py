import time
from app.rag.rag_pipeline import RAGPipeline

# Couleurs pour la console (optionnel mais pratique)
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_separator():
    print("-" * 80)

def run_scenario(pipeline, scenario_name, questions):
    print(f"\n{Colors.HEADER}{Colors.BOLD}=== SCÉNARIO : {scenario_name} ==={Colors.ENDC}\n")
    
    # On réinitialise l'historique à chaque scénario
    pipeline.chat_history = []
    
    for i, question in enumerate(questions):
        print(f"{Colors.OKCYAN}{Colors.BOLD}Utilisateur :{Colors.ENDC} {question}")
        
        start_time = time.time()
        try:
            response, docs = pipeline.ask(question)
            elapsed_time = time.time() - start_time
            
            print(f"{Colors.OKGREEN}{Colors.BOLD}Assistant ({elapsed_time:.2f}s) :{Colors.ENDC} {response}\n")
            
            if docs:
                print(f"{Colors.WARNING}Sources trouvées ({len(docs)}) :{Colors.ENDC}")
                for j, doc in enumerate(docs[:3]): # On n'affiche que les 3 premières pour pas flood
                    source = doc.metadata.get("source", "Inconnu")
                    preview = doc.page_content[:80].replace('\n', ' ') + "..."
                    print(f"  [{j+1}] {source} -- {preview}")
            else:
                print(f"{Colors.FAIL}Aucune source trouvée.{Colors.ENDC}")
                
        except Exception as e:
            print(f"{Colors.FAIL}ERREUR : {e}{Colors.ENDC}")
            
        print_separator()
        time.sleep(1) # Petit délai pour ne pas saturer Ollama

def main():
    print(f"{Colors.HEADER}Initialisation du pipeline RAG...{Colors.ENDC}")
    pipeline = RAGPipeline(retrieval_top_k=5) # Top_k réduit pour accélérer les tests
    print(f"{Colors.HEADER}Pipeline prêt !{Colors.ENDC}")
    print_separator()

    # --- DÉFINITION DES SCÉNARIOS DE TEST ---

    # Test 1 : Recherche factuelle classique (Le livre parle beaucoup du mensonge)
    test_1 = [
        "Quels sont les signes du mensonge selon le livre ?"
    ]

    # Test 2 : Question de suivi + Reformulation (Le cœur de notre architecture)
    test_2 = [
        "Que dit le livre sur le toucher du nez ?",
        "Quelles en sont les implications ?" # Devrait être reformulé en "Implications du toucher du nez"
        "Donne moi un exemple concret." # Devrait être reformulé en "Exemple concret de toucher du nez"
    ]

    # Test 3 : Recherche sur un autre chapitre (Séduction/Flirt - Chapitre 9)
    test_3 = [
        "Comment les femmes montrent-elles qu'elles sont intéressées sexuellement ?"
    ]

    # Test 4 : Anti-hallucination (Hors-sujet total)
    test_4 = [
        "Comment faire une blanquette de veau ?" # Doit répondre "Je ne trouve pas..."
    ]

    # Test 5 : Entité spécifique (Le livre mentionne Bernadette et Nietzsche dans les chunks)
    test_5 = [
        "Que dit le texte sur Bernadette ?"
    ]

    # --- EXÉCUTION DES TESTS ---
    run_scenario(pipeline, "1. Recherche Factuelle (Mensonge)", test_1)
    run_scenario(pipeline, "2. Contextualisation et Reformulation", test_2)
    run_scenario(pipeline, "3. Autre Chapitre (Séduction)", test_3)
    run_scenario(pipeline, "4. Anti-Hallucination (Hors-sujet)", test_4)
    run_scenario(pipeline, "5. Entité Spécifique (Bernadette)", test_5)

    print(f"\n{Colors.HEADER}{Colors.BOLD}=== FIN DES TESTS ==={Colors.ENDC}")

if __name__ == "__main__":
    main()