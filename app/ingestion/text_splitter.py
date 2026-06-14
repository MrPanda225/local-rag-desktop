"""Module for splitting documents into Parent and Child chunks."""
import uuid
from typing import List

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


class ParentChildSplitter:  # pylint: disable=too-few-public-methods
    """
    Splits documents into Parent chunks (large) and Child chunks (small).
    Children inherit the ID of their Parent for 'Small-to-Big' retrieval.
    """

    def __init__(self, parent_size: int = 1500, parent_overlap: int = 300,
                 child_size: int = 400, child_overlap: int = 80):
        separators = ["\n\n", "\n", ". ", " ", ""]

        self.parent_splitter = RecursiveCharacterTextSplitter(
            chunk_size=parent_size, chunk_overlap=parent_overlap, separators=separators
        )
        self.child_splitter = RecursiveCharacterTextSplitter(
            chunk_size=child_size, chunk_overlap=child_overlap, separators=separators
        )

    def split(self, docs: List[Document]) -> List[Document]:
        """Split documents into Parents and Children and assign matching IDs."""
        parent_docs = self.parent_splitter.split_documents(docs)
        all_docs = []

        for parent in parent_docs:
            parent_id = str(uuid.uuid4())
            parent.metadata["doc_id"] = parent_id
            parent.metadata["type"] = "parent"
            all_docs.append(parent)

            child_docs = self.child_splitter.split_documents([parent])
            for child in child_docs:
                child_id = str(uuid.uuid4())
                child.metadata["doc_id"] = child_id
                child.metadata["parent_id"] = parent_id
                child.metadata["type"] = "child"
                all_docs.append(child)

        return all_docs
