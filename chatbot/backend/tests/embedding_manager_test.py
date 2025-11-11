# -*- coding: utf-8 -*-
"""
embedding_manager_test.py

Unit test for EmbeddingManager functionality.
- Initializes required managers and models
- Creates example local and web documents
- Queries embeddings and prints results
"""

from langchain_core.documents import Document
from src.utils.embedding_manager import EmbeddingManager
from src.utils.key_manager import KeyManager
from src.utils.gemini_model_manager import ModelManager

# Initialize KeyManager (handles API keys or credentials)
key_manager = KeyManager()

# Initialize ModelManager and obtain the embedding model
model_manager = ModelManager()
embedding_model = model_manager.embeddings  # Ensure 'embeddings' attribute exists

# Example local documents (replace with real data as needed)
local_documents = [
    Document(page_content="Contenido del manual 1"),
    Document(page_content="Contenido del manual 2"),
]

# Example web documents (replace with real data as needed)
web_documents = [
    Document(page_content="Artículo web 1 sobre regresión"),
    Document(page_content="Artículo web 2 sobre regresión"),
]

# Create an instance of EmbeddingManager
embedding_manager = EmbeddingManager(
    embedding_model=embedding_model,
    local_documents=local_documents,
    web_documents=web_documents,
    persist_directory="./src/database",  # Directory for Chroma DB persistence
)

# Query the embeddings with a sample question
query = "What is regression?"
results = embedding_manager.query_embeddings(
    query=query, k=1  # Set k=3 to retrieve top 3 relevant documents
)

# Print the content of the most relevant documents
for result in results:
    print(result.page_content)
