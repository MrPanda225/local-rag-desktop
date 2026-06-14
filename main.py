# main.py
from app.rag.rag_pipeline import RAGPipeline
from app.ui.desktop import RAGDesktopApp

if __name__ == "__main__":
    pipeline = RAGPipeline()
    app = RAGDesktopApp(rag_pipeline=pipeline)
    app.run()