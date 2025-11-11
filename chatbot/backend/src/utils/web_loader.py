# -*- coding: utf-8 -*-
"""
File: web_loader.py

This file contains the WebLoader class, responsible for fetching, parsing,
and converting web pages into markdown documents. It uses concurrent futures
to handle multiple URLs simultaneously and BeautifulSoup for HTML parsing.
"""

from concurrent.futures import ThreadPoolExecutor, as_completed, Future
from typing import List, Optional, Dict, Sequence

import requests
from bs4 import BeautifulSoup

from langchain_core.documents import Document
from langchain_community.document_transformers.markdownify import MarkdownifyTransformer

from src.config.config_init import MARKDOWNIFY_CONFIG
from src.utils.logger_manager import logger


class WebLoader:
    def __init__(self, urls: List[str]) -> None:
        """
        Initializes the WebLoader instance with a list of URLs to process.

        Args:
            urls (List[str]): List of URLs to be fetched and converted to Markdown.
        """
        self.urls: List[str] = urls

    def get_documents(self) -> List[Document]:
        """
        Fetches and parses the list of URLs, returning a list of Document objects.
        Retries up to 3 times for each URL that fails.

        Returns:
            List[Document]: A list of Document objects containing the content of the parsed web pages.
        """
        documents: List[Document] = []
        max_retries: int = 3
        url_attempts: Dict[str, int] = {url: 0 for url in self.urls}
        remaining_urls: set[str] = set(self.urls)

        while remaining_urls:
            remaining_urls = self._process_url_batch(
                remaining_urls, url_attempts, max_retries, documents
            )
        logger.info(f"All documents loaded: {len(documents)}")
        return documents

    def _process_url_batch(
        self,
        urls: set[str],
        url_attempts: Dict[str, int],
        max_retries: int,
        documents: List[Document],
    ) -> set[str]:
        """
        Processes a batch of URLs concurrently using a thread pool.
        Submits each URL to be fetched and parsed, then collects results as they complete.
        Updates the documents list with successful loads and tracks failed URLs for retry.

        Args:
            urls (set[str]): Set of URLs to process in this batch.
            url_attempts (Dict[str, int]): Tracks the number of attempts for each URL.
            max_retries (int): Maximum number of retries per URL.
            documents (List[Document]): List to append successfully loaded documents to.

        Returns:
            set[str]: Set of URLs that failed in this batch and should be retried.
        """
        failed_urls: set[str] = set()
        with ThreadPoolExecutor(max_workers=20) as executor:
            future_to_url = self._submit_url_futures(urls, executor)
            for future in as_completed(future_to_url):
                url = future_to_url[future]
                self._handle_future_result(
                    future, url, documents, url_attempts, max_retries, failed_urls
                )
        return failed_urls

    def _submit_url_futures(
        self, urls: set[str], executor: ThreadPoolExecutor
    ) -> Dict[Future[Optional[Document]], str]:
        """
        Submits fetch_and_parse tasks for each URL to the thread pool executor.
        Returns a mapping from Future objects to their corresponding URLs for tracking.

        Args:
            urls (set[str]): Set of URLs to submit as tasks.
            executor (ThreadPoolExecutor): The thread pool executor instance.

        Returns:
            Dict[Future[Optional[Document]], str]: Mapping from Future to URL.
        """
        return {executor.submit(self._fetch_and_parse, url): url for url in urls}

    def _handle_future_result(
        self,
        future: Future[Optional[Document]],
        url: str,
        documents: List[Document],
        url_attempts: Dict[str, int],
        max_retries: int,
        failed_urls: set[str],
    ) -> None:
        """
        Handles the result of a completed future for a URL fetch/parse task.
        If successful, appends the document to the documents list and marks the URL as done.
        If failed, increments the attempt count and adds to failed_urls if retries remain.
        Logs errors and warnings as appropriate.

        Args:
            future (Future[Optional[Document]]): The completed future object.
            url (str): The URL associated with this future.
            documents (List[Document]): List to append successful documents to.
            url_attempts (Dict[str, int]): Tracks the number of attempts for each URL.
            max_retries (int): Maximum number of retries per URL.
            failed_urls (set[str]): Set to add failed URLs to for retrying.
        """
        try:
            logger.info(f"Loading URL: {url[-30:]}")
            document: Optional[Document] = future.result()
            if document:
                documents.append(document)
                url_attempts[url] = max_retries  # Mark as done
            else:
                url_attempts[url] += 1
                if url_attempts[url] < max_retries:
                    failed_urls.add(url)
                else:
                    logger.warning(
                        f"Failed to load URL after {max_retries} attempts: {url}"
                    )
        except Exception as e:
            url_attempts[url] += 1
            if url_attempts[url] < max_retries:
                failed_urls.add(url)
            else:
                logger.error(
                    f"Error getting document for URL {url} after {max_retries} attempts: {e}"
                )

    def _fetch_and_parse(self, url: str) -> Optional[Document]:
        """
        Fetches, parses, and converts the HTML content of a URL into a Markdown document.

        Args:
            url (str): The URL to fetch and process.

        Returns:
            Optional[Document]: A Document object if successful, None otherwise.
        """
        try:
            logger.debug(f"Start fetch_and_parse for: {url}")
            html_content: Optional[str] = self._fetch_html(url)
            if not html_content:
                logger.error(f"No HTML content for: {url}")
                return None

            soup: Optional[BeautifulSoup] = self._parse_html(html_content)
            if not soup:
                logger.error(f"No soup for: {url}")
                return None

            article_html: Optional[str] = self._extract_article(soup)
            if not article_html:
                logger.error(f"No article found for: {url}")
                return None

            markdown_content: str = self._convert_to_markdown(article_html)
            metadata: Dict[str, str] = self._extract_metadata(soup, url)
            metadata["html_content_length"] = str(len(markdown_content))

            logger.debug(f"Document created for: {url}")
            return self._create_document(markdown_content, metadata)
        except Exception as e:
            logger.error(f"Error fetching and parsing URL {url}: {e}")
            return None

    def _fetch_html(self, url: str) -> Optional[str]:
        """
        Fetches the HTML content of a given URL.

        Args:
            url (str): The URL to fetch.

        Returns:
            Optional[str]: The HTML content of the page if successful, None otherwise.
        """
        try:
            logger.debug(f"Fetching URL: {url}")
            response: requests.Response = requests.get(url, timeout=10)
            response.raise_for_status()
            logger.info(f"Fetched URL successfully: {url[-30:]}")
            return response.text
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching URL {url}: {e}")
            return None

    def _parse_html(self, html: str) -> Optional[BeautifulSoup]:
        """
        Parses the HTML content and returns a BeautifulSoup object.

        Args:
            html (str): The HTML content of the page.

        Returns:
            Optional[BeautifulSoup]: A BeautifulSoup object if parsing is successful, None otherwise.
        """
        try:
            return BeautifulSoup(html, "html.parser") if html else None
        except Exception as e:
            logger.error(f"Error parsing HTML: {e}")
            return None

    def _extract_article(self, soup: BeautifulSoup) -> Optional[str]:
        """
        Extracts the main article content from the parsed HTML.

        Args:
            soup (BeautifulSoup): A BeautifulSoup object containing the parsed HTML.

        Returns:
            Optional[str]: The HTML content of the article section if found, None otherwise.
        """
        try:
            article_section: Optional[BeautifulSoup] = soup.find(
                "article", class_="bd-article"
            )  # type: ignore
            if article_section:
                gallery_examples_section: Optional[BeautifulSoup] = article_section.find("section", id="gallery-examples")  # type: ignore
                if gallery_examples_section:
                    gallery_examples_section.decompose()  # Remove the gallery section
                return str(article_section)
            return None
        except Exception as e:
            logger.error(f"Error extracting article: {e}")
            return None

    def _extract_metadata(self, soup: BeautifulSoup, url: str) -> Dict[str, str]:
        """
        Extracts metadata from the HTML, such as the page title.

        Args:
            soup (BeautifulSoup): A BeautifulSoup object containing the parsed HTML.
            url (str): The URL of the web page.

        Returns:
            Dict[str, str]: A dictionary containing metadata, including the URL and title of the page.
        """
        try:
            title: str = soup.find("title").text if soup.find("title") else "No title"  # type: ignore
            return {"url": url, "title": title}
        except Exception as e:
            logger.error(f"Error extracting metadata: {e}")
            return {"url": url, "title": "No title"}

    def _convert_to_markdown(self, html_content: str) -> str:
        """
        Converts the HTML content to Markdown using the Markdownify transformer.

        Args:
            html_content (str): The HTML content to be converted to Markdown.

        Returns:
            str: The content converted to Markdown.
        """
        try:
            html_document: Document = Document(page_content=html_content)
            transformer: MarkdownifyTransformer = MarkdownifyTransformer(
                **MARKDOWNIFY_CONFIG
            )
            markdown_content: Sequence[Document] = transformer.transform_documents(
                [html_document]
            )
            return str(markdown_content[0])
        except Exception as e:
            logger.error(f"Error converting to Markdown: {e}")
            return ""

    def _create_document(self, html_content: str, metadata: Dict[str, str]) -> Document:
        """
        Creates a Document object from the HTML content and metadata.

        Args:
            html_content (str): The content of the document.
            metadata (Dict[str, str]): Metadata related to the document.

        Returns:
            Document: The created Document object.
        """
        try:
            return Document(page_content=html_content, metadata=metadata)
        except Exception as e:
            logger.error(f"Error creating document: {e}")
            return Document(page_content="", metadata=metadata)
