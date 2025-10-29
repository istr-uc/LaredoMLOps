# -*- coding: utf-8 -*-
"""
File: main.py

This script initializes and runs the chatbot system by setting up core components
and executing a test conversation.
"""
from src.chatbot.core_initializer import CoreInitializer
from src.config.config_url import DOCS_URL
from src.chatbot.graph_initializer import GraphInitializer
from src.chatbot.chat_initializer import ChatInitializer

# Define paths for documents
DOCS_PATH = "./docs"  # Local directory containing documents
WEB_PATHS = DOCS_URL  # List of web document URLs


def main() -> None:
    """
    Initializes the chatbot system and starts a conversation.

    This function sets up the core components of the chatbot, creates the chatbot graph,
    and starts a conversation using the initialized components.
    """
    # Initialize core components (LLM, embeddings, etc.)
    core = CoreInitializer(docs_path=DOCS_PATH, web_paths=WEB_PATHS)
    core.initialize()

    # Retrieve initialized managers
    model_manager = core.model_manager
    embedding_manager = core.embedding_manager

    # Create and compile the chatbot graph
    chatbot_graph = GraphInitializer(
        model_manager=model_manager, embedding_manager=embedding_manager
    )
    chatbot_graph.build_graph()

    # Configure and start the chatbot conversation
    config = {"configurable": {"thread_id": "1"}}
    chatbot = ChatInitializer(chatbot_graph=chatbot_graph, config=config)

    # chatbot.start_conversation()

    import asyncio

    asyncio.run(chatbot.start_conversation_chunks())


if __name__ == "__main__":
    main()
