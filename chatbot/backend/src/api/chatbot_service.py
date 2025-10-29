# -*- coding: utf-8 -*-
"""
chatbot_service.py

Service class for chatbot initialization and response generation.

This module defines the ChatbotService class, which manages the setup of core chatbot components, builds the chatbot graph, and provides methods for generating responses to user questions (including streaming responses).
"""

from typing import AsyncGenerator, List, Any, Dict

from src.chatbot.core_initializer import CoreInitializer
from src.config.config_url import DOCS_URL
from src.chatbot.graph_initializer import GraphInitializer


class ChatbotService:
    """
    Service class for managing chatbot initialization and response generation.

    This class sets up the core components of the chatbot, builds the chatbot graph, and provides methods to generate responses (both standard and streaming) to user questions.
    """

    def __init__(
        self, docs_path: str = "./docs", web_paths: List[str] = DOCS_URL
    ) -> None:
        """
        Initialize the chatbot system and start a conversation.

        Args:
            docs_path (str): Path to the documentation directory. Defaults to './docs'.
            web_paths (List[str]): List of web documentation URLs. Defaults to DOCS_URL.

        This method sets up the core components (LLM, embeddings, etc.), retrieves the initialized managers, builds the chatbot graph, and configures the chatbot conversation.
        """
        # Initialize core components (LLM, embeddings, etc.)
        core = CoreInitializer(docs_path=docs_path, web_paths=web_paths)
        core.initialize()

        # Retrieve initialized managers
        model_manager = core.model_manager
        embedding_manager = core.embedding_manager

        # Create and compile the chatbot graph
        self.chatbot_graph: GraphInitializer = GraphInitializer(
            model_manager=model_manager, embedding_manager=embedding_manager
        )
        self.chatbot_graph.build_graph()

        # Configure and start the chatbot conversation
        self.config = {"configurable": {"thread_id": "1"}}

    async def generate_response(self, question: str) -> str:
        """
        Generate a response to a user's question.

        Args:
            question (str): The user's question.
        Returns:
            str: The chatbot's answer.
        """
        response: Dict[str, Any] = await self.chatbot_graph.graph.invoke(  # type: ignore
            {"question": question}, self.config
        )
        return response["answer"]  # type: ignore

    async def generate_response_stream(
        self, question: str
    ) -> AsyncGenerator[str, None]:
        """
        Generate a streaming response to a user's question.

        Args:
            question (str): The user's question.
        Yields:
            str: Chunks of the chatbot's answer, delimited by <END_OF_CHUNK>.
        """
        async for event in self.chatbot_graph.graph.astream_events(  # type: ignore
            {"question": question}, self.config
        ):
            # Only yield content from the 'generate_answer' node stream events
            if (
                event["event"] == "on_chat_model_stream"
                and event["metadata"].get("langgraph_node", "") == "generate_answer"  # type: ignore
            ):
                data: Any = event["data"]  # type: ignore
                content: str = getattr(data["chunk"], "content", "")  # type: ignore
                if content:
                    yield f"data: {content}\n\n<END_OF_CHUNK>"  # Add delimiter for each chunk
