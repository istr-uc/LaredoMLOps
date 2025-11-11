# -*- coding: utf-8 -*-
"""
Test file for the ModelManager class (Ollama integration).
This script demonstrates how to use the ModelManager to:
- Generate a response from the LLM model.
- Generate an embedding vector from a sample query.
"""

from src.utils.ollama_model_manager import ModelManager


def main():
    # Instantiate the ModelManager (handles LLM and embeddings)
    model_manager = ModelManager()

    # Test the LLM model with a sample prompt
    test_prompt = "Hello, how are you?"
    response = model_manager.llm.invoke([{"role": "user", "content": test_prompt}])
    print(f"LLM Response: {response}")

    # Test the embeddings model with a sample query
    test_embedding = model_manager.embeddings.embed_query("What's our Q1 revenue?")
    print(f"Embedding Sample (first 10 values): {test_embedding[:10]}")


if __name__ == "__main__":
    main()
