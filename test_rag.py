"""Automated test suite for the RAG pipeline."""
import time
from app.rag.rag_pipeline import RAGPipeline


class Colors:  # pylint: disable=too-few-public-methods
    """ANSI color codes for terminal output."""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def print_separator():
    """Print a visual separator line in the console."""
    print("-" * 80)


def run_scenario(pipeline, scenario_name, questions):
    """Run a list of questions against the pipeline and display results."""
    print(
        f"\n{Colors.HEADER}{Colors.BOLD}"
        f"=== SCÉNARIO : {scenario_name} ==="
        f"{Colors.ENDC}\n"
    )

    pipeline.chat_history = []

    for question in questions:
        print(f"{Colors.OKCYAN}{Colors.BOLD}Utilisateur :{Colors.ENDC} {question}")

        start_time = time.time()
        try:
            response, docs = pipeline.ask(question)
            elapsed_time = time.time() - start_time

            print(
                f"{Colors.OKGREEN}{Colors.BOLD}Assistant "
                f"({elapsed_time:.2f}s) :{Colors.ENDC} {response}\n"
            )

            if docs:
                print(f"{Colors.WARNING}Sources trouvées ({len(docs)}) :{Colors.ENDC}")
                for j, doc in enumerate(docs[:3]):
                    source = doc.metadata.get("source", "Inconnu")
                    preview = doc.page_content[:80].replace('\n', ' ') + "..."
                    print(f"  [{j+1}] {source} -- {preview}")
            else:
                print(f"{Colors.FAIL}Aucune source trouvée.{Colors.ENDC}")

        except Exception as exc:  # pylint: disable=broad-exception-caught
            print(f"{Colors.FAIL}ERREUR : {exc}{Colors.ENDC}")

        print_separator()
        time.sleep(1)


def main():
    """Execute the main test suite."""
    print(f"{Colors.HEADER}Initialisation du pipeline RAG...{Colors.ENDC}")
    pipeline = RAGPipeline(retrieval_top_k=5)
    print(f"{Colors.HEADER}Pipeline prêt !{Colors.ENDC}")
    print_separator()

    test_1 = ["Quels sont les signes du mensonge selon le livre ?"]
    test_2 = [
        "Que dit le livre sur le toucher du nez ?",
        "Quelles en sont les implications ?",
        "Donne moi un exemple concret."
    ]
    test_3 = ["Comment les femmes montrent-elles qu'elles sont intéressées sexuellement ?"]
    test_4 = ["Comment faire une blanquette de veau ?"]
    test_5 = ["Que dit le texte sur Bernadette ?"]

    run_scenario(pipeline, "1. Recherche Factuelle (Mensonge)", test_1)
    run_scenario(pipeline, "2. Contextualisation et Reformulation", test_2)
    run_scenario(pipeline, "3. Autre Chapitre (Séduction)", test_3)
    run_scenario(pipeline, "4. Anti-Hallucination (Hors-sujet)", test_4)
    run_scenario(pipeline, "5. Entité Spécifique (Bernadette)", test_5)

    print(f"\n{Colors.HEADER}{Colors.BOLD}=== FIN DES TESTS ==={Colors.ENDC}")


if __name__ == "__main__":
    main()