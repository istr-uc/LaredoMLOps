# -*- coding: utf-8 -*-
"""
File: core_initializer.py

This file contains the CoreInitializer class, responsible for initializing
the key components of the application. It loads necessary services such as
API keys, models, documents, and embeddings before the main process begins.
"""

from typing import List
from src.utils.key_manager import KeyManager
from src.utils.gemini_model_manager import ModelManager
from src.utils.embedding_manager import EmbeddingManager
from src.utils.document_manager import DocumentManager
from src.utils.logger_manager import logger


class CoreInitializer:
    def __init__(self, docs_path: str, web_paths: List[str]) -> None:
        """
        Initializes the application with paths for local and web documents.

        Args:
            docs_path (str): Local path where documents are stored.
            web_paths (List[str]): List of URLs to web documents.
        """
        self._docs_path: str = docs_path
        self._web_paths: List[str] = web_paths
        self._model_manager: ModelManager | None = None
        self._document_manager: DocumentManager | None = None
        self._embedding_manager: EmbeddingManager | None = None

    def initialize(self) -> None:
        """
        Initializes the key components of the application.
        """
        try:
            # Initializing KeyManager, ModelManager, DocumentManager, and EmbeddingManager
            KeyManager()
            self._model_manager = ModelManager()
            self._document_manager = DocumentManager(
                directory_path=self._docs_path, web_paths=self._web_paths
            )
            self._embedding_manager = EmbeddingManager(
                embedding_model=self._model_manager.embeddings,
                local_documents=self._document_manager.local_sections,
                web_documents=self._document_manager.web_sections,
            )

            # Log successful initialization
            logger.info("Core initialized successfully.")
        except Exception as e:
            # Log any errors encountered during initialization
            logger.error(f"Error during core initialization: {e}")
            raise

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
