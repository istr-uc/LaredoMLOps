# -*- coding: utf-8 -*-
"""
Test file for the ModelManeger class.
"""

from src.utils.gemini_model_manager import ModelManager
from src.utils.key_manager import KeyManager


def main():
    # install keys
    KeyManager()
    # Create a ModelManager instance
    model_manager = ModelManager()

    # Test the LLM model
    test_prompt = "Hello, how are you?"
    response = model_manager.llm.invoke(test_prompt)  # type: ignore
    print(f"LLM Response: {response}")

    # Test the embeddings model
    test_embedding = model_manager.embeddings.embed_query("What's our Q1 revenue?")  # type: ignore
    print(f"Embedding Sample: {test_embedding[:10]}")


if __name__ == "__main__":
    main()
