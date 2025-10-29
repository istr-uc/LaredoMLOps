# -*- coding: utf-8 -*-
"""
File: directory_loader.py

This file defines the DirectoryLoader class, responsible for loading Markdown documents
from a specified directory.
"""

import os
import concurrent.futures
from typing import List

from langchain_core.documents import Document
from src.utils.logger_manager import logger


class DirectoryLoader:
    def __init__(
        self, directory_path: str, markdown_files_extension: str = ".md"
    ) -> None:
        """
        Initializes the DirectoryLoader instance.

        Args:
            directory_path (str): The path to the directory where Markdown files are stored.
            markdown_files_extension (str): The file extension used to identify Markdown files. Default is ".md".
        """
        self._directory_path: str = directory_path
        self._markdown_files_extension: str = markdown_files_extension
        self._local_documents: List[Document] = []

    def _read_file(self, file_path: str, file_name: str) -> Document:
        """
        Reads a Markdown file and creates a Document object containing its content and metadata.

        Args:
            file_path (str): The full path to the Markdown file.
            file_name (str): The name of the Markdown file.

        Returns:
            Document: A Document object containing the file's content and metadata.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                file_content: str = file.read()
                return Document(
                    page_content=file_content, metadata={"file_name": file_name}
                )
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
            raise

    def _load_local_documents(self) -> None:
        """
        Loads the Markdown documents from the specified directory in parallel.

        This method scans the directory for Markdown files, reads them concurrently,
        and stores the resulting documents.
        """
        if not self._directory_path:
            logger.error("The 'directory_path' must be provided.")
            raise ValueError("The 'directory_path' must be provided.")

        # Check if the directory exists
        if not os.path.exists(self._directory_path):
            logger.error(f"Directory not found: {self._directory_path}")
            raise FileNotFoundError(f"Directory not found: {self._directory_path}")

        # List of Markdown file paths
        markdown_files: List[str] = [
            os.path.join(self._directory_path, file_name)
            for file_name in os.listdir(self._directory_path)
            if file_name.endswith(self._markdown_files_extension)
        ]

        if not markdown_files:
            logger.warning(
                f"No Markdown files found in the directory: {self._directory_path}"
            )

        # Process files in parallel using ThreadPoolExecutor
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self._read_file, file_path, os.path.basename(file_path))
                for file_path in markdown_files
            ]

            # Wait for all futures to complete and append the documents to the list
            for future in concurrent.futures.as_completed(futures):
                try:
                    self._local_documents.append(future.result())
                except Exception as e:
                    logger.error(f"Error processing file: {e}")

    def get_documents(self) -> List[Document]:
        """
        Returns the loaded Markdown documents.

        If documents have not been loaded yet, this method will load them from the specified directory.

        Returns:
            List[Document]: A list of Document objects containing the content of Markdown files.
        """
        if not self._local_documents:
            try:
                self._load_local_documents()
            except Exception as e:
                logger.error(f"Error loading documents: {e}")
                return []
        return self._local_documents
