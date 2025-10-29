# -*- coding: utf-8 -*-
"""
File: document_manager.py

This file defines the DocumentManager class, responsible for managing the loading
and splitting of Markdown and web documents.
"""

import concurrent.futures
from typing import List, Optional

from langchain.text_splitter import MarkdownTextSplitter
from langchain_core.documents import Document

from src.config.config_init import MARKDOWN_SPLITTER_CONFIG
from src.utils.logger_manager import logger
from src.utils.directory_loader import DirectoryLoader
from src.utils.web_loader import WebLoader

import re


class DocumentManager:
    """
    Manages the loading and splitting of Markdown and web documents from a specified directory.
    """

    def __init__(
        self,
        directory_path: Optional[str] = None,
        web_paths: Optional[List[str]] = None,
        plain_words_only: bool = True,
    ) -> None:
        """
        Initializes the DocumentManager by loading and splitting documents.

        Args:
            directory_path (Optional[str]): Path to the directory containing Markdown files.
            web_paths (Optional[List[str]]): List of web document URLs.
            plain_words_only (bool): If True, sections will be converted to plain words only.

        Raises:
            ValueError: If neither 'directory_path' nor 'web_paths' is provided.
        """

        if directory_path is None and web_paths is None:
            raise ValueError("Either directory_path or web_paths must be provided.")

        self._directory_path = directory_path
        self._local_documents: List[Document] = []
        self._local_sections: List[Document] = []

        self.web_paths = web_paths
        self._web_documents: List[Document] = []
        self._web_sections: List[Document] = []

        self._plain_words_only = plain_words_only

        # Execute loading and splitting in parallel
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.submit(self._load_and_split_local_documents)
            executor.submit(self._load_and_split_web_documents)

    def _load_and_split_local_documents(self) -> None:
        """Loads and splits the local Markdown documents."""
        logger.info("Loading local documents...")
        self._load_local_documents()
        logger.info(f"Loaded {len(self._local_documents)} documents.")

        logger.info("Splitting local documents...")
        self._split_local_documents()
        logger.info(f"Split local documents into {len(self._local_sections)} sections.")

    def _load_and_split_web_documents(self) -> None:
        """Loads and splits the web documents."""
        logger.info("Loading web documents...")
        self._load_web_documents()
        logger.info(f"Loaded {len(self._web_documents)} web documents.")

        logger.info("Splitting web documents...")
        self._split_web_documents()
        logger.info(f"Split web documents into {len(self._web_sections)} sections.")

    def _load_local_documents(self) -> None:
        """Loads the Markdown documents from the specified directory."""
        if self._directory_path is None:
            raise ValueError("directory_path must be provided.")
        loader = DirectoryLoader(
            directory_path=self._directory_path, markdown_files_extension=".md"
        )
        self._local_documents = loader.get_documents()

    def _load_web_documents(self) -> None:
        """Loads the web documents from the specified URLs."""
        if self.web_paths is None:
            raise ValueError("web_paths must be provided.")
        loader = WebLoader(urls=self.web_paths)
        self._web_documents = loader.get_documents()

    def _process_section(self, section: str) -> str:
        """Process a section according to the plain_words_only flag, cleaning markdown
        symbols, images, links, tables, footnotes, and formatting text."""
        if self._plain_words_only:
            text = section
            # Remove code blocks (```...``` including content)
            text = re.sub(r"```[\s\S]*?```", "", text)
            # Remove images ![alt](url)
            text = re.sub(r"!\[[^\]]*\]\([^\)]*\)", "", text)
            # Remove links [text](url)
            text = re.sub(r"\[[^\]]*\]\([^\)]*\)", "", text)
            # Remove double-bracket links [[text]](url)
            text = re.sub(r"\[\[[^\]]*\]\]\([^\)]*\)", "", text)
            # Remove reference-style links [text][id]
            text = re.sub(r"\[[^\]]*\]\[[^\]]*\]", "", text)
            # Remove footnote references [^1]
            text = re.sub(r"\[\^\d+\]", "", text)
            # Remove tables (lines starting/containing |)
            text = re.sub(r"^\s*\|.*\|\s*$", "", text, flags=re.MULTILINE)
            # Remove table header separators (| --- |)
            text = re.sub(r"^\s*\|?\s*:?-+:?\s*\|.*$", "", text, flags=re.MULTILINE)
            # Remove HTML tags
            text = re.sub(r"<[^>]+>", "", text)
            # Remove headers (#, ##, ###, etc.)
            text = re.sub(r"^#+\s*", "", text, flags=re.MULTILINE)
            # Remove emphasis (*, _, **, __)
            text = re.sub(r"(\*\*|__|\*|_)", "", text)
            # Remove inline code/backticks
            text = re.sub(r"`+", "", text)
            # Remove blockquotes
            text = re.sub(r"^>\s*", "", text, flags=re.MULTILINE)
            # Remove unordered list markers (-, *, + at line start)
            text = re.sub(r"^(\s*[-*+])\s+", "", text, flags=re.MULTILINE)
            # Remove ordered list markers (1. 2. etc.)
            # text = re.sub(r"^\s*\d+\.\s+", "", text, flags=re.MULTILINE)
            # Remove horizontal rules
            text = re.sub(r"^---+$", "", text, flags=re.MULTILINE)
            # Remove extra newlines and trim
            text = re.sub(r"\n+", "\n", text)
            # Remove extra tabs and trim
            text = re.sub(r"\t+", "\t", text)
            text = text.strip()
            return text
        return section

    def _split_local_documents(self) -> None:
        """Splits the local documents into sections, optionally as plain words only."""
        splitter: MarkdownTextSplitter = MarkdownTextSplitter(
            **MARKDOWN_SPLITTER_CONFIG
        )
        for doc in self._local_documents:
            split_sections: List[str] = splitter.split_text(doc.page_content)
            for section in split_sections:
                processed_section: str = self._process_section(section)
                self._local_sections.append(
                    Document(page_content=processed_section, metadata=doc.metadata)  # type: ignore
                )

    def _split_web_documents(self) -> None:
        """Splits the web documents into sections, optionally as plain words only."""
        splitter: MarkdownTextSplitter = MarkdownTextSplitter(
            **MARKDOWN_SPLITTER_CONFIG
        )
        for doc in self._web_documents:
            split_sections: List[str] = splitter.split_text(doc.page_content)
            for section in split_sections:
                processed_section: str = self._process_section(section)
                self._web_sections.append(
                    Document(page_content=processed_section, metadata=doc.metadata)  # type: ignore
                )

    @property
    def local_documents(self) -> List[Document]:
        """Gets the loaded local documents."""
        return self._local_documents

    @property
    def local_sections(self) -> List[Document]:
        """Gets the split sections of the local documents."""
        return self._local_sections

    @property
    def web_documents(self) -> List[Document]:
        """Gets the loaded web documents."""
        return self._web_documents

    @property
    def web_sections(self) -> List[Document]:
        """Gets the split sections of the web documents."""
        return self._web_sections
