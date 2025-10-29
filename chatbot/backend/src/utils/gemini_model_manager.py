# -*- coding: utf-8 -*-
"""
File: gemini_model_manager.py

This module defines the ModelManager class, responsible for managing the
initialization of the Gemini language model (LLM) and embeddings.
"""
import concurrent.futures
from typing import Optional

from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

from src.config.config_init import LLM_CONFIG, EMBEDDINGS_CONFIG, LLM_FLASH_CONFIG
from src.utils.logger_manager import logger


class ModelManager:
    """
    Manages the creation and access of the default LLM, flash LLM, and embeddings models.
    """
    def __init__(self) -> None:
        """
        Initializes the default LLM, flash LLM, and embeddings models asynchronously.
        Each LLM gets its own rate limiter based on config.
        """
        logger.info("Initializing ModelManager...")
        self._llm: Optional[ChatGoogleGenerativeAI] = None
        self._flash_llm: Optional[ChatGoogleGenerativeAI] = None
        self._embeddings: Optional[GoogleGenerativeAIEmbeddings] = None

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_llm = executor.submit(self._initialize_llm, LLM_CONFIG)
            future_flash_llm = executor.submit(self._initialize_llm, LLM_FLASH_CONFIG)
            future_embeddings = executor.submit(self._initialize_embeddings)

            self._llm = future_llm.result()
            self._flash_llm = future_flash_llm.result()
            self._embeddings = future_embeddings.result()

        logger.info("ModelManager initialized successfully.")

    def _initialize_llm(self, config) -> Optional[ChatGoogleGenerativeAI]:
        """
        Initializes the Gemini LLM model, handling exceptions.

        Returns:
            Optional[ChatGoogleGenerativeAI]: Instance of the LLM model if successful, else None.
        """
        try:
            logger.info("Initializing LLM model (Gemini)...")
            return ChatGoogleGenerativeAI(**config)
        except Exception as e:
            logger.error(f"Failed to initialize LLM model: {e}")
            return None

    def _initialize_embeddings(self) -> Optional[GoogleGenerativeAIEmbeddings]:
        """
        Initializes the Gemini embeddings model, handling exceptions.

        Returns:
            Optional[GoogleGenerativeAIEmbeddings]: Instance of the embeddings model if successful, else None.
        """
        try:
            logger.info("Initializing embeddings model (Gemini)...")
            return GoogleGenerativeAIEmbeddings(**EMBEDDINGS_CONFIG)
        except Exception as e:
            logger.error(f"Failed to initialize embeddings model: {e}")
            return None

    @property
    def llm(self) -> Optional[ChatGoogleGenerativeAI]:
        """
        Getter for the default LLM model.

        Returns:
            Optional[ChatGoogleGenerativeAI]: Instance of the language model if initialized.
        """
        if self._llm is None:
            logger.warning("Attempted to access uninitialized default LLM model.")
        return self._llm

    @property
    def flash_llm(self) -> Optional[ChatGoogleGenerativeAI]:
        """
        Getter for the Flash LLM model (used for translation and summarization).

        Returns:
            Optional[ChatGoogleGenerativeAI]: Instance of the Flash LLM model if initialized.
        """
        if self._flash_llm is None:
            logger.warning("Attempted to access uninitialized Flash LLM model.")
        return self._flash_llm

    @property
    def embeddings(self) -> Optional[GoogleGenerativeAIEmbeddings]:
        """
        Getter for the embeddings model.

        Returns:
            Optional[GoogleGenerativeAIEmbeddings]: Instance of the embeddings model if initialized.
        """
        if self._embeddings is None:
            logger.warning("Attempted to access uninitialized embeddings model.")
        return self._embeddings
