import os
from langchain_chroma import Chroma
from langchain_community.retrievers import BM25Retriever
from flashrank import Ranker, RerankRequest
from langchain_core.documents import Document

class Retriever:
    """Récupère les chunks via recherche hybride, expansion Parent-Child, et Reranking."""

    def __init__(self, embeddings, db_folder: str = "db", top_k: int = 4):
        self.db_folder = db_folder
        self.top_k = top_k
        self.embedder = embeddings
        
        self.db = Chroma(
            persist_directory=self.db_folder,
            embedding_function=self.embedder,
        )
        
        # BM25 est nourri avec Parents ET Enfants
        all_data = self.db._collection.get(include=["documents", "metadatas"])
        bm25_docs = [
            Document(page_content=doc, metadata=meta) 
            for doc, meta in zip(all_data["documents"], all_data["metadatas"])
        ]
        
        self.bm25_retriever = None
        if bm25_docs:
            self.bm25_retriever = BM25Retriever.from_documents(bm25_docs)
            self.bm25_retriever.k = top_k * 5 

        self.ranker = Ranker(max_length=512)

    def search(self, query: str):
        fetch_k = self.top_k * 5

        # 1. Recherche Chroma (Sémantique) - ON RETIRE LE FILTRE DE SCORE
        # On fait confiance au Reranker pour trier le bon grain de l'ivraie
        chroma_docs = self.db.similarity_search(query, k=fetch_k)
        
        # 2. Recherche BM25 (Mots-clés)
        bm25_docs = []
        if self.bm25_retriever:
            bm25_docs = self.bm25_retriever.invoke(query)
            
        # 3. EXPANSION PARENT-CHILD
        parent_ids_to_fetch = set()
        child_docs_fallback = []
        direct_parent_hits = []
        
        # On fusionne les résultats de Chroma et BM25
        for doc in chroma_docs + bm25_docs:
            doc_type = doc.metadata.get("type", "parent")
            
            if doc_type == "child":
                parent_id = doc.metadata.get("parent_id")
                if parent_id:
                    parent_ids_to_fetch.add(parent_id)
                    child_docs_fallback.append(doc)
                else:
                    direct_parent_hits.append(doc)
            else:
                direct_parent_hits.append(doc)

        # On va chercher les Parents manquants dans Chroma via l'API bas niveau
        if parent_ids_to_fetch:
            try:
                fetched_parents = self.db._collection.get(ids=list(parent_ids_to_fetch), include=["documents", "metadatas"])
                for text, meta in zip(fetched_parents["documents"], fetched_parents["metadatas"]):
                    direct_parent_hits.append(Document(page_content=text, metadata=meta))
            except Exception:
                direct_parent_hits.extend(child_docs_fallback)

        # 4. Dédoublonnage des Parents
        seen_doc_ids = set()
        merged_docs = []
        for doc in direct_parent_hits:
            doc_id = doc.metadata.get("doc_id")
            if doc_id and doc_id not in seen_doc_ids:
                seen_doc_ids.add(doc_id)
                merged_docs.append(doc)
            elif not doc_id:
                merged_docs.append(doc)
                
        if not merged_docs:
            return []

        # 5. Reranking sur les PARENTS uniquement
        passages = [{"id": i, "text": doc.page_content} for i, doc in enumerate(merged_docs)]
        rerank_request = RerankRequest(query=query, passages=passages)
        ranked_results = self.ranker.rerank(rerank_request)
        
        final_docs = []
        for result in ranked_results[:self.top_k]:
            original_index = result["id"]
            final_docs.append(merged_docs[original_index])
        
        return final_docs