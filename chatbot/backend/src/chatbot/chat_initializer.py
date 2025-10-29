# -*- coding: utf-8 -*-
"""
File: chat_initializer.py

This module defines the ChatInitializer class, which manages the interaction loop
between the user and the chatbot, handling user input and responses.
"""

from typing import Any, Dict
from src.utils.logger_manager import logger


class ChatInitializer:
    """
    Handles the chatbot interaction loop, managing user input and response handling.
    """

    def __init__(self, chatbot_graph: Any, config: Dict[str, Any]) -> None:
        """
        Initializes the chatbot interaction manager.

        Args:
            chatbot_graph: The structured graph managing chatbot logic.
            config: Configuration settings for chatbot execution.
        """
        self._chatbot_graph = chatbot_graph
        self._config = config

    def start_conversation(self) -> None:
        """
        Initiates the chatbot conversation loop, continuously handling user input and displaying responses.
        """
        logger.info("Starting the conversation loop.")

        while True:
            user_input: str = input("You: ")  # Prompt the user for input

            if user_input.lower() in {"exit", "quit"}:
                logger.info("User ended the conversation.")  # Log when the user exits
                break  # Exit the loop and end the conversation

            input_message = user_input

            # Execute the graph without streaming
            response = self._chatbot_graph.graph.invoke(
                {"question": input_message}, self._config
            )
            response_message = response["answer"]
            print(response_message)

    async def start_conversation_chunks(self) -> None:
        """
        Initiates the chatbot conversation loop, continuously handling user input and displaying responses.
        """
        logger.info("Starting the conversation loop.")

        while True:
            user_input: str = input("You: ")  # Prompt the user for input

            if user_input.lower() in {"exit", "quit"}:
                logger.info("User ended the conversation.")  # Log when the user exits
                break  # Exit the loop and end the conversation

            input_message = user_input

            print("Bot:", end=" ", flush=True)  # Imprime "Bot:" sin salto de línea

            async for event in self._chatbot_graph.graph.astream_events(
                {"question": input_message}, self._config
            ):
                # Get chat model tokens from a particular node
                if (
                    event["event"] == "on_chat_model_stream"
                    and event["metadata"].get("langgraph_node", "") == "generate_answer"
                ):
                    data = event["data"]
                    print(data["chunk"].content, end="")
            print()  # Print a newline after the response
