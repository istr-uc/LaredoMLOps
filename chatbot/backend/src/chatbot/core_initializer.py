# -*- coding: utf-8 -*-
"""
File: core_initializer.py

This file contains the CoreInitializer class, responsible for initializing
the key components of the application. It loads necessary services such as
API keys, models, documents, and embeddings before the main process begins.
"""

import os
from typing import List
from src.utils.key_manager import KeyManager
from src.utils.gemini_model_manager import ModelManager
from src.utils.ollama_model_manager import ModelManager as OllamaModelManager
from src.utils.embedding_manager import EmbeddingManager
from src.utils.document_manager import DocumentManager
from src.utils.logger_manager import logger


class CoreInitializer:
    def __init__(self, docs_path: str, web_paths: List[str], skip_db_init: bool = False) -> None:
        """
        Initializes the application with paths for local and web documents.

        Args:
            docs_path (str): Local path where documents are stored.
            web_paths (List[str]): List of URLs to web documents.
            skip_db_init (bool): If True and database exists, skip database initialization.
                                If False, always initialize the database. Defaults to False.
        """
        self._docs_path: str = docs_path
        self._web_paths: List[str] = web_paths
        self._skip_db_init: bool = skip_db_init
        self._model_manager: ModelManager | None = None
        self._document_manager: DocumentManager | None = None
        self._embedding_manager: EmbeddingManager | None = None
        self._ollama_model_manager: OllamaModelManager | None = None

    def initialize(self) -> None:
        """
        Initializes the key components of the application.
        
        If skip_db_init is True and a database exists, the EmbeddingManager 
        initialization is skipped to reuse the pre-initialized database.
        Other components (ModelManager, OllamaModelManager) are always initialized.
        """
        try:
            # Initializing KeyManager, ModelManager, and OllamaModelManager
            KeyManager(env_file="environment/.env")
            self._model_manager = ModelManager()
            self._ollama_model_manager = OllamaModelManager()
            
            # Check if we should skip database initialization
            db_exists = self._database_exists()
            should_skip_db = self._skip_db_init and db_exists
            
            if should_skip_db:
                logger.info("Pre-initialized database detected. Skipping database initialization.")
                logger.info("Using existing Chroma database from disk.")
                # Create a minimal EmbeddingManager that loads without resetting
                self._embedding_manager = self._create_embedding_manager_for_existing_db()
            else:
                if self._skip_db_init and not db_exists:
                    logger.warning(
                        "skip_db_init is True but no database found. "
                        "Initializing database from scratch."
                    )
                # Full initialization: load documents and create embeddings
                self._document_manager = DocumentManager(
                    directory_path=self._docs_path, web_paths=self._web_paths
                )
                self._embedding_manager = EmbeddingManager(
                    embedding_model=self._ollama_model_manager.embeddings,
                    local_documents=self._document_manager.local_sections,
                    web_documents=self._document_manager.web_sections,
                )

            # Log successful initialization
            logger.info("Core initialized successfully.")
        except Exception as e:
            # Log any errors encountered during initialization
            logger.error(f"Error during core initialization: {e}")
            raise

    def _database_exists(self) -> bool:
        """
        Checks if a Chroma database already exists at the default location.
        
        Returns:
            bool: True if database directory exists and contains database files, False otherwise.
        """
        import os
        db_path = "./database"
        if os.path.exists(db_path) and os.path.isdir(db_path):
            # Check if there are any files in the database directory (indicating it's not empty)
            return len(os.listdir(db_path)) > 0
        return False

    def _create_embedding_manager_for_existing_db(self) -> EmbeddingManager:
        """
        Creates an EmbeddingManager that loads an existing Chroma database without resetting it.
        
        This is used when skip_db_init is True and a database already exists.
        It avoids expensive document loading and embedding generation.
        
        Returns:
            EmbeddingManager: An embedding manager with empty document lists (database will be loaded from disk).
        """
        from typing import List as TypeList
        from langchain_core.documents import Document as LangChainDoc
        
        # Create with empty document lists to avoid re-indexing
        empty_local_docs: TypeList[LangChainDoc] = []
        empty_web_docs: TypeList[LangChainDoc] = []
        
        # The EmbeddingManager will still load the Chroma database from disk
        # but won't create new collections since document lists are empty
        try:
            # Create a temporary EmbeddingManager with minimal setup
            # Note: We'll create it but override the reset behavior
            embedding_manager = EmbeddingManager(
                embedding_model=self._ollama_model_manager.embeddings,
                local_documents=empty_local_docs,
                web_documents=empty_web_docs,
                persist_directory="./database",
                skip_reset=True  # Custom flag to skip reset in this case
            )
            
            # The database will load from disk; collections should already exist
            # If collections don't exist (shouldn't happen with pre-init), this will create empty ones
            logger.info("Loaded existing Chroma database from disk.")
            return embedding_manager
            
        except Exception as e:
            logger.error(f"Failed to load existing database: {e}")
            logger.warning("Falling back to full database initialization.")
            # Fall back to full initialization
            self._document_manager = DocumentManager(
                directory_path=self._docs_path, web_paths=self._web_paths
            )
            return EmbeddingManager(
                embedding_model=self._ollama_model_manager.embeddings,
                local_documents=self._document_manager.local_sections,
                web_documents=self._document_manager.web_sections,
                skip_reset=False,
            )

    @property
    def model_manager(self) -> ModelManager:
        """
        Returns the ModelManager instance.
        """
        return self._model_manager  # type: ignore

    @property
    def document_manager(self) -> DocumentManager:
        """
        Returns the DocumentManager instance.
        """
        return self._document_manager  # type: ignore

    @property
    def embedding_manager(self) -> EmbeddingManager:
        """
        Returns the EmbeddingManager instance.
        """
        return self._embedding_manager  # type: ignore
