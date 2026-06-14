"""Module for hybrid search, parent-child expansion, and reranking."""
from langchain_chroma import Chroma
from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document
from flashrank import Ranker, RerankRequest


class Retriever:  # pylint: disable=too-few-public-methods
    """Retrieves chunks via hybrid search, parent expansion, and reranking."""

    def __init__(self, embeddings, db_folder: str = "db", top_k: int = 4):
        self.db_folder = db_folder
        self.top_k = top_k
        self.embedder = embeddings

        self.db = Chroma(
            persist_directory=self.db_folder,
            embedding_function=self.embedder,
        )

        all_data = self.db._collection.get(include=["documents", "metadatas"])  # pylint: disable=protected-access
        bm25_docs = [
            Document(page_content=doc, metadata=meta)
            for doc, meta in zip(all_data["documents"], all_data["metadatas"])
        ]

        self.bm25_retriever = None
        if bm25_docs:
            self.bm25_retriever = BM25Retriever.from_documents(bm25_docs)
            self.bm25_retriever.k = top_k * 5

        self.ranker = Ranker(max_length=512)

    def search(self, query: str):  # pylint: disable=too-many-locals,too-many-branches
        """Search Chroma, expand to parents, deduplicate, and rerank."""
        fetch_k = self.top_k * 5

        chroma_docs = self.db.similarity_search(query, k=fetch_k)

        bm25_docs = []
        if self.bm25_retriever:
            bm25_docs = self.bm25_retriever.invoke(query)

        parent_ids_to_fetch = set()
        child_docs_fallback = []
        direct_parent_hits = []

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

        if parent_ids_to_fetch:
            try:
                fetched_parents = self.db._collection.get(  # pylint: disable=protected-access
                    ids=list(parent_ids_to_fetch),
                    include=["documents", "metadatas"]
                )
                for text, meta in zip(
                    fetched_parents["documents"], fetched_parents["metadatas"]
                ):
                    direct_parent_hits.append(
                        Document(page_content=text, metadata=meta)
                    )
            except Exception:  # pylint: disable=broad-exception-caught
                direct_parent_hits.extend(child_docs_fallback)

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

        passages = [
            {"id": i, "text": doc.page_content}
            for i, doc in enumerate(merged_docs)
        ]
        rerank_request = RerankRequest(query=query, passages=passages)
        ranked_results = self.ranker.rerank(rerank_request)

        final_docs = []
        for result in ranked_results[:self.top_k]:
            original_index = result["id"]
            final_docs.append(merged_docs[original_index])

        return final_docs
