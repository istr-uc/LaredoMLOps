# -*- coding: utf-8 -*-
"""
File: config_init.py

This file defines the configurations used for document loading with DirectoryLoader
and the configuration options for the LLM model.
"""

from typing import Dict, Any

# -----------------------------
# Markdown-related Configuration
# -----------------------------

MARKDOWNIFY_CONFIG: Dict[str, Any] = {
    "split": ["dl", "dt", "dd"],  # Tags to split the content
    "heading_style": "ATX",  # Heading style (ATX for # headers)
}

MARKDOWN_SPLITTER_CONFIG: Dict[str, Any] = {
    "chunk_size": 1000,  # Maximum size of each chunk
    "chunk_overlap": 200,  # Overlap between chunks to maintain context
    "keep_separator": True,  # Include separators in the resulting chunks
}

# -------------------------
# LLM (Language Model) Configuration
# -------------------------

LLM_CONFIG: Dict[str, Any] = {
    "model": "gemini-2.0-flash",  # Google Gemini model
    "temperature": 0.2,  # Lower creativity for more factual responses
    "top_p": 0.85,  # Controls response diversity
    "top_k": 40,  # Filters top candidate tokens at each step
    "max_tokens": 2048,  # Maximum response length
    "disable_streaming": "tool_calling",  # Enable streaming, except when calling external tools
    "verbose": False,  # Disable detailed logs in production
    "max_retries": 3,  # Number of retries in case of failure
    "timeout": 30.0,  # Maximum wait time for a response
}

LLM_FLASH_CONFIG = {
    "model": "gemini-2.0-flash-lite",  # Google Gemini model
    "temperature": 0,  # Lower creativity for more factual responses
    "top_p": 0.85,  # Controls response diversity
    "top_k": 40,  # Filters top candidate tokens at each step
    "max_tokens": 1024,  # Maximum response length
    "disable_streaming": "tool_calling",  # Enable streaming, except when calling external tools
    "verbose": False,  # Disable detailed logs in production
    "max_retries": 3,  # Number of retries in case of failure
    "timeout": 30.0,  # Maximum wait time for a response
}

# -------------------------
# Embeddings Configuration
# -------------------------

EMBEDDINGS_CONFIG: Dict[str, Any] = {
    "model": "models/text-embedding-004",  # Name of the embeddings model
    "task_type": "retrieval_document",  # Set if needed for a specific task
    "client_options": None,  # Advanced client configuration
    "transport": None,  # Custom transport method
    "request_options": None,  # Additional request options
}

# -------------------------
# Chroma Database Configuration
# -------------------------

CHROMA_DB_CONFIG: Dict[str, Any] = {
    "client_settings": None,  # Additional client settings, if needed
    "client": None,  # Custom client for accessing the Chroma database (if any)
    "relevance_score_fn": None,  # Custom relevance scoring function (if used)
    "create_collection_if_not_exists": True,  # Create the collection if it doesn't exist
}

# -----------------------------
# Logger Configuration
# -----------------------------
LOGGER_LEVEL = "INFO"

# -------------------------
# Search Configuration
# -------------------------
K_WEB_SEARCH = 1  # Default number of web documents to retrieve

K_LOCAL_SEARCH = 3  # Default number of local documents to retrieve

# -------------------------
# Flask Configuration
# -------------------------
FLASK_PORT = 20000

FLASK_DEBUG = False
