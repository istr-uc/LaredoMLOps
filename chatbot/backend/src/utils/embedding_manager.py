# -*- coding: utf-8 -*-
"""
File: embedding_manager.py

This file defines the EmbeddingManager class, which is responsible for managing
document embeddings and storing them in the Chroma database. The embeddings are
organized into two collections: one for local documents and one for web documents.
The class provides functionality to query these collections for relevant embeddings.
"""

from concurrent.futures import ThreadPoolExecutor
from typing import List, Optional, Any


from langchain_chroma import Chroma
from langchain_core.documents import Document

from src.config.config_init import CHROMA_DB_CONFIG
from src.utils.logger_manager import logger


class EmbeddingManager:
    """
    The EmbeddingManager is responsible for managing embeddings stored in a Chroma
    database, separated into two collections: one for local documents and another
    for web documents.
    """

    def __init__(
        self,
        embedding_model: Any,
        local_documents: List[Document],
        web_documents: List[Document],
        persist_directory: str = "./database",
    ) -> None:
        """
        Initializes the EmbeddingManager, which manages embeddings for local and web
        documents, and initializes the Chroma database and collections.

        Args:
            embedding_model (Embeddings): The model used to generate embeddings.
            local_documents (List[Document]): Local documents to index.
            web_documents (List[Document]): Web documents to index.
            persist_directory (str): Directory to store the Chroma database.
        """
        self.embedding_model = embedding_model
        self.local_documents = local_documents
        self.web_documents = web_documents
        self.persist_directory = persist_directory

        self.database: Optional[Chroma] = None
        self.local_collection: Optional[Chroma] = None
        self.web_collection: Optional[Chroma] = None

        self.local_collection_name = "local_documents"
        self.web_collection_name = "web_documents"

        # Initialize the database and collections
        self._initialize_database()

    def _initialize_database(self) -> None:
        """
        Initializes the Chroma database and its collections. If the `reset_database`
        flag is set to True, the database will be deleted and recreated.

        This method also initializes the collections for local and web documents in parallel.
        """
        logger.info("Initializing database...")

        # Reset the database if required
        self._reset_database()

        # Load the Chroma database
        self.database = Chroma(
            embedding_function=self.embedding_model,
            persist_directory=self.persist_directory,
            **CHROMA_DB_CONFIG,
        )

        # Initialize collections in parallel using ThreadPoolExecutor
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(
                    self._get_chroma_collection,
                    self.local_collection_name,
                    self.local_documents,
                ),
                executor.submit(
                    self._get_chroma_collection,
                    self.web_collection_name,
                    self.web_documents,
                ),
            ]
            results = [future.result() for future in futures]
            self.local_collection, self.web_collection = results

        logger.info("Database and collections initialized successfully.")

    def _reset_database(self) -> None:
        """
        Deletes the existing Chroma database at the specified `persist_directory` and
        recreates it from scratch. Tries 3 times; if it fails, logs a warning and continues.
        """
        import shutil
        import os
        from src.utils.logger_manager import logger

        max_retries = 3
        for attempt in range(max_retries):
            try:
                if os.path.exists(self.persist_directory):
                    logger.info(
                        f"Deleting existing database at {self.persist_directory}..."
                    )
                    shutil.rmtree(self.persist_directory)
                break
            except Exception as e:
                logger.warning(
                    f"Attempt {attempt+1}/{max_retries} to delete database failed: {e}"
                )
        else:
            logger.warning(
                "Could not reset the database after 3 attempts. Continuing execution."
            )
        os.makedirs(self.persist_directory, exist_ok=True)

    def _get_chroma_collection(
        self, collection_name: str, documents: List[Document]
    ) -> Chroma:
        """
        Loads an existing Chroma collection or creates a new one if it doesn't exist.

        Args:
            collection_name (str): The name of the collection to load or create.
            documents (List[Document]): The documents to index in the collection.

        Returns:
            Chroma: The Chroma collection object.
        """
        logger.info(f"Loading or creating Chroma collection '{collection_name}'...")

        # Chroma automatically creates the collection if it doesn't exist
        collection = Chroma.from_documents(  # type: ignore
            documents=documents,
            embedding=self.embedding_model,
            persist_directory=self.persist_directory,
            collection_name=collection_name,
        )

        logger.info(f"Chroma collection '{collection_name}' is ready.")
        return collection

    def query_local_embeddings(self, query: str, k: int) -> List[Document]:
        """
        Queries the local collection for relevant embeddings.

        Args:
            query (str): The query string to search for in the local collection.
            k (int): The number of most similar documents to return.

        Returns:
            List[Document]: A list of the most relevant documents from the local collection.
        """
        logger.debug(f"Querying local embeddings for: {query} with k={k}")

        # Perform similarity search on the local collection
        results = self.local_collection.similarity_search(query, k)  # type: ignore

        for result in results:
            logger.debug(
                f"Found local document: {result.page_content[:50]} and {result.id}"
            )

        return results

    def query_web_embeddings(self, query: str, k: int) -> List[Document]:
        """
        Queries the web collection for relevant embeddings.

        Args:
            query (str): The query string to search for in the web collection.
            k (int): The number of most similar documents to return.

        Returns:
            List[Document]: A list of the most relevant documents from the web collection.
        """
        logger.debug(f"Querying web embeddings for: {query} with k={k}")

        # Perform similarity search on the web collection
        results = self.web_collection.similarity_search(query, k)  # type: ignore

        for result in results:
            logger.debug(
                f"Found web document: {result.page_content[:50]} and {result.id}"
            )

        return results

    def query_embeddings(self, query: str, k: int) -> List[Document]:
        """
        Queries both the local and web collections for relevant embeddings.

        Args:
            query (str): The query string to search for in both collections.
            k (int): The number of most similar documents to return from each collection.

        Returns:
            List[Document]: A combined list of relevant documents from both collections.
        """
        logger.debug(f"Querying all collections for: {query} with k={k}")

        # Use ThreadPoolExecutor to parallelize similarity search across collections
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self.query_local_embeddings, query, k),
                executor.submit(self.query_web_embeddings, query, k),
            ]
            results = [future.result() for future in futures]

        # Combine results from both collections
        all_results = results[0] + results[1]

        return all_results
