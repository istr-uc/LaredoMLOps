# -*- coding: utf-8 -*-
"""
document_manager_test.py

Unit test for DocumentManager functionality.
- Loads and splits local documents from the docs directory
- Loads and splits web documents from URLs in DOCS_URL
- Prints summary statistics for loaded and split documents
"""

from src.utils.document_manager import DocumentManager
from src.config.config_url import DOCS_URL


def main():
    # Test loading and splitting local documents
    document_manager = DocumentManager(directory_path="./docs")
    print(f"Loaded {len(document_manager.local_documents)} local documents.")
    print(f"Split into {len(document_manager.local_sections)} local sections.")

    # Test loading and splitting web documents
    web_paths = DOCS_URL
    document_manager_web = DocumentManager(web_paths=web_paths)
    print(f"Loaded {len(document_manager_web.web_documents)} web documents.")
    print(f"Split into {len(document_manager_web.web_sections)} web sections.")

    # Uncomment below to inspect document content samples
    # print(document_manager_web.web_documents[1])
    # print("Local DOCS Sections:")
    # for section in document_manager.local_sections:
    #     print(section.page_content[:1000])  # Print the first 1000 characters of each section

    # print("WEB Sections:")
    # for section in document_manager_web.web_sections:
    #     print(section.page_content[:100])  # Print the first 100 characters of each section


if __name__ == "__main__":
    main()
