# -*- coding: utf-8 -*-
"""
init_chroma_db.py

Standalone script to pre-initialize the Chroma database with document embeddings
before containerization. This avoids the overhead of database initialization during
container startup.

Usage:
    python init_chroma_db.py [--docs-path DOCS_PATH] [--db-path DB_PATH] [--no-reset]

Arguments:
    --docs-path     Path to the documentation directory (default: ../backend/docs)
    --db-path       Path where the Chroma database will be stored (default: ../backend/database)
    --no-reset      Don't delete existing database; append to it instead (default: delete and recreate)

Example:
    # Initialize with default paths (docs from ../backend/docs, output to ../backend/database)
    python init_chroma_db.py

    # Use custom paths
    python init_chroma_db.py --docs-path /path/to/docs --db-path /path/to/database

    # Append to existing database instead of recreating
    python init_chroma_db.py --no-reset
"""

import sys
import os
import argparse
import logging
from pathlib import Path
from typing import List, Optional

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from langchain_core.documents import Document
from src.utils.embedding_manager import EmbeddingManager
from src.utils.document_manager import DocumentManager
from src.utils.ollama_model_manager import ModelManager as OllamaModelManager
from src.utils.logger_manager import logger


class ChromaDatabaseInitializer:
    """
    Initializes a Chroma database locally with embedded documents.
    """

    def __init__(
        self,
        docs_path: str = "./docs",
        db_path: str = "./database",
        reset_database: bool = True,
    ) -> None:
        """
        Initialize the ChromaDatabaseInitializer.

        Args:
            docs_path (str): Path to the documentation directory.
            db_path (str): Path where the Chroma database will be stored.
            reset_database (bool): Whether to delete and recreate the database (True) or append (False).
        """
        self.docs_path = docs_path
        self.db_path = db_path
        self.reset_database = reset_database
        self.embedding_manager: Optional[EmbeddingManager] = None

        # Validate paths
        if not os.path.exists(self.docs_path):
            raise ValueError(f"Documentation directory not found: {self.docs_path}")

        logger.info(
            f"Initializing Chroma database at {self.db_path} with docs from {self.docs_path}"
        )
        if self.reset_database:
            logger.info("Database will be reset (deleted and recreated)")
        else:
            logger.info("Database will be appended to (not reset)")

    def initialize(self) -> None:
        """
        Performs the full initialization: loads documents, initializes embeddings model,
        and creates the Chroma database with collections.
        """
        try:
            # Step 1: Initialize the Ollama embeddings model
            logger.info("Step 1/3: Initializing Ollama embeddings model...")
            ollama_model_manager = OllamaModelManager()
            embedding_model = ollama_model_manager.embeddings
            logger.info("✓ Ollama embeddings model initialized")

            # Step 2: Load and split documents
            logger.info("Step 2/3: Loading and splitting documents from docs directory...")
            document_manager = DocumentManager(
                directory_path=self.docs_path,
                web_paths=None,  # No web documents for pre-initialization
                plain_words_only=True,
            )
            local_sections = document_manager.local_sections
            logger.info(
                f"✓ Loaded and split documents into {len(local_sections)} sections"
            )

            # Step 3: Initialize Chroma database with embeddings
            logger.info(
                "Step 3/3: Creating Chroma database and embedding documents (this may take a while)..."
            )

            # Create empty web documents list for compatibility
            empty_web_documents: List[Document] = []

            # Create EmbeddingManager with skip_reset based on the reset_database flag
            # If reset_database is True, skip_reset is False (will delete and recreate)
            # If reset_database is False, skip_reset is True (will append to existing)
            self.embedding_manager = EmbeddingManager(
                embedding_model=embedding_model,
                local_documents=local_sections,
                web_documents=empty_web_documents,
                persist_directory=self.db_path,
                skip_reset=not self.reset_database,
            )

            logger.info("✓ Chroma database initialized successfully")
            logger.info(
                f"Database location: {os.path.abspath(self.db_path)}"
            )
            logger.info(f"Collections created: 'local_documents', 'web_documents'")

        except Exception as e:
            logger.error(f"Failed to initialize Chroma database: {e}")
            raise


def main() -> int:
    """
    Main entry point for the script.

    Returns:
        int: 0 on success, 1 on failure.
    """
    parser = argparse.ArgumentParser(
        description="Pre-initialize Chroma database with document embeddings",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Initialize with default paths (../backend/docs -> ../backend/database)
  python init_chroma_db.py

  # Use custom paths
  python init_chroma_db.py --docs-path /path/to/docs --db-path /path/to/database

  # Append to existing database instead of recreating
  python init_chroma_db.py --no-reset
        """,
    )

    parser.add_argument(
        "--docs-path",
        type=str,
        default=os.path.join(os.path.dirname(__file__), "..", "backend", "docs"),
        help="Path to the documentation directory (default: ../backend/docs)",
    )

    parser.add_argument(
        "--db-path",
        type=str,
        default=os.path.join(os.path.dirname(__file__), "..", "backend", "database"),
        help="Path where the Chroma database will be stored (default: ../backend/database)",
    )

    parser.add_argument(
        "--no-reset",
        action="store_true",
        help="Don't delete existing database; append to it instead (default: reset)",
    )

    args = parser.parse_args()

    # Resolve paths to absolute
    docs_path = os.path.abspath(args.docs_path)
    db_path = os.path.abspath(args.db_path)
    reset_database = not args.no_reset

    logger.info("=" * 80)
    logger.info("Chroma Database Pre-Initialization Script")
    logger.info("=" * 80)
    logger.info(f"Documentation path: {docs_path}")
    logger.info(f"Database path: {db_path}")
    logger.info(f"Reset existing database: {reset_database}")
    logger.info("=" * 80)

    try:
        initializer = ChromaDatabaseInitializer(
            docs_path=docs_path, db_path=db_path, reset_database=reset_database
        )
        initializer.initialize()

        logger.info("=" * 80)
        logger.info("✓ Chroma database initialization completed successfully!")
        logger.info("=" * 80)
        logger.info("You can now build the Docker image and COPY the database directory:")
        logger.info(f"  COPY {db_path} /project/database/")
        logger.info("=" * 80)

        return 0

    except Exception as e:
        logger.error("=" * 80)
        logger.error("✗ Chroma database initialization failed!")
        logger.error("=" * 80)
        logger.error(f"Error: {e}")
        logger.error("=" * 80)
        return 1


if __name__ == "__main__":
    sys.exit(main())
