# -*- coding: utf-8 -*-
"""
File: ollama_model_manager.py

This file contains the ModelManager class, responsible for managing the creation
of language models (LLM) and embeddings using Ollama.
"""

from src.utils.logger_manager import logger

from langchain_ollama import ChatOllama, OllamaEmbeddings

# TODO: Uncomment the following import when the config file is available
# from src.config.config import LLM_CONFIG, EMBEDDINGS_CONFIG

# discontinued :/


class ModelManager:
    """
    Class to manage the creation of LLM and embeddings models.
    """

    def __init__(self):
        """
        Constructor of the class. Initializes the LLM and embeddings models.
        """

        logger.info("Initializing ModelManager...")

        # check if the models are already initialized to avoid reinitialization
        self._llm = self._llm if hasattr(self, "_llm") else self._initialize_llm()
        self._embeddings = (
            self._embeddings
            if hasattr(self, "_embeddings")
            else self._initialize_embeddings()
        )

        logger.info("ModelManager initialized successfully.")

    def _initialize_llm(self) -> ChatOllama:
        """
        Initializes the Ollama LLM model for text generation.

        Returns:
            ChatOllama: Instance of the language model.
        """
        logger.info("Initializing LLM model (Ollama)...")
        return ChatOllama(model="gemma3:4b")

    def _initialize_embeddings(self) -> OllamaEmbeddings:
        """
        Initializes the Ollama embeddings model for generating vector representations.

        Returns:
            OllamaEmbeddings: Instance of the embeddings model.
        """
        logger.info("Initializing embeddings model (Ollama)...")
        return OllamaEmbeddings(model="nomic-embed-text:latest")

    # ----------------------------------------------------------------------------------------------
    # Getters and setters

    @property
    def llm(self) -> ChatOllama:
        """Getter for the LLM model."""
        return self._llm

    @property
    def embeddings(self) -> OllamaEmbeddings:
        """Getter for the embeddings model."""
        return self._embeddings
