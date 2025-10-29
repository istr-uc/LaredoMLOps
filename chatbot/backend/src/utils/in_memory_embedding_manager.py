# -*- coding: utf-8 -*-
"""
File: in_memory_embedding_manager.py

This file defines the InMemoryEmbeddingManager class, which is responsible for managing
in-memory document embeddings using InMemoryVectorStore from langchain_core. The embeddings are
organized into two stores: one for local documents and one for web documents.
The class provides functionality to query these stores for relevant embeddings.
Suitable for prototyping, testing, or use cases where persistence is not required.
"""

from concurrent.futures import ThreadPoolExecutor
from typing import List, Optional, Any

from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.documents import Document
from src.utils.logger_manager import logger

class InMemoryEmbeddingManager:
    """
    The InMemoryEmbeddingManager is responsible for managing embeddings stored in memory,
    separated into two stores: one for local documents and another for web documents.
    """

    def __init__(
        self,
        embedding_model: Any,
        local_documents: List[Document],
        web_documents: List[Document],
    ) -> None:
        """
        Initializes the InMemoryEmbeddingManager, which manages embeddings for local and web
        documents, and initializes the in-memory stores.

        Args:
            embedding_model (Embeddings): The model used to generate embeddings.
            local_documents (List[Document]): Local documents to index.
            web_documents (List[Document]): Web documents to index.
        """
        self.embedding_model = embedding_model
        self.local_documents = local_documents
        self.web_documents = web_documents

        self.local_store: Optional[InMemoryVectorStore] = None
        self.web_store: Optional[InMemoryVectorStore] = None

        # Initialize the in-memory stores
        self._initialize_stores()

    def _initialize_stores(self) -> None:
        """
        Initializes the in-memory vector stores for local and web documents in parallel.
        """
        logger.info("Initializing in-memory vector stores for local and web documents...")
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(
                    InMemoryVectorStore.from_documents,
                    self.local_documents,
                    self.embedding_model,
                ),
                executor.submit(
                    InMemoryVectorStore.from_documents,
                    self.web_documents,
                    self.embedding_model,
                ),
            ]
            results = [future.result() for future in futures]
            self.local_store, self.web_store = results
        logger.info("In-memory vector stores initialized successfully.")

    def query_local_embeddings(self, query: str, k: int) -> List[Document]:
        """
        Queries the local in-memory store for relevant embeddings.

        Args:
            query (str): The query string to search for in the local store.
            k (int): The number of most similar documents to return.

        Returns:
            List[Document]: A list of the most relevant documents from the local store.
        """
        logger.debug(f"Querying local in-memory embeddings for: {query} with k={k}")
        if not self.local_store:
            return []
        results = self.local_store.similarity_search(query, k=k)
        for result in results:
            logger.debug(
                f"Found local document: {result.page_content[:50]} and {getattr(result, 'id', None)}"
            )
        return results

    def query_web_embeddings(self, query: str, k: int) -> List[Document]:
        """
        Queries the web in-memory store for relevant embeddings.

        Args:
            query (str): The query string to search for in the web store.
            k (int): The number of most similar documents to return.

        Returns:
            List[Document]: A list of the most relevant documents from the web store.
        """
        logger.debug(f"Querying web in-memory embeddings for: {query} with k={k}")
        if not self.web_store:
            return []
        results = self.web_store.similarity_search(query, k=k)
        for result in results:
            logger.debug(
                f"Found web document: {result.page_content[:50]} and {getattr(result, 'id', None)}"
            )
        return results

    def query_embeddings(self, query: str, k: int) -> List[Document]:
        """
        Queries both the local and web in-memory stores for relevant embeddings.

        Args:
            query (str): The query string to search for in both stores.
            k (int): The number of most similar documents to return from each store.

        Returns:
            List[Document]: A combined list of relevant documents from both stores.
        """
        logger.debug(f"Querying all in-memory stores for: {query} with k={k}")
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self.query_local_embeddings, query, k),
                executor.submit(self.query_web_embeddings, query, k),
            ]
            results = [future.result() for future in futures]
        all_results = results[0] + results[1]
        return all_results
