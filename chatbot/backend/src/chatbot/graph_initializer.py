# -*- coding: utf-8 -*-
"""
File: graph_initializer.py

This file contains the GraphInitializer class, responsible for managing the chatbot's
graph logic, including searching for context, generating answers using a language model,
and summarizing the conversation. It integrates different components like a model manager,
embedding manager, and utility functions to process questions and generate appropriate responses.
"""

import json
import re

from typing import List, Dict, Union, TypedDict

from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import (
    HumanMessage,
    SystemMessage,
    RemoveMessage,
    BaseMessage,
    MessageLikeRepresentation,
)
from langchain_core.documents import Document

from src.utils.gemini_model_manager import ModelManager
from src.utils.embedding_manager import EmbeddingManager
from src.utils.logger_manager import logger
from src.config.config_chatbot import (
    SUMMARY_PROMPT,
    RECENT_MESSAGES_PROMPT,
    ANSWER_PROMPT,
    SUMMARIZATION_PROMPT,
    TRANSLATE_OPTIMIZE_QUESTION_PROMPT,
)
from src.config.config_init import K_WEB_SEARCH, K_LOCAL_SEARCH


# States for each graph to modularize
class InputState(TypedDict):
    question: str


class TranslateState(TypedDict):
    question: MessageLikeRepresentation


class SearchState(TypedDict):
    question: MessageLikeRepresentation
    local_context: List[Document]
    web_context: List[Document]
    language: str  # Nuevo campo para el idioma


class GenerationState(MessagesState):
    question: MessageLikeRepresentation  # The user's question
    answer: MessageLikeRepresentation  # The generated answer to the question
    local_context: List[Document]  # Local context (local document search results)
    web_context: List[Document]  # Web context (web search results)
    summary: str  # Summary of previous conversation (if available)
    language: str  # Nuevo campo para el idioma


class SummarizationState(MessagesState):
    answer: MessageLikeRepresentation  # The generated answer to the question
    summary: str
    documents: List[Document]


class OutputState(TypedDict):
    answer: str
    documents: List[Document]


class JsonState(TypedDict):
    improved_question: MessageLikeRepresentation


class GraphInitializer:
    def __init__(
        self, model_manager: ModelManager, embedding_manager: EmbeddingManager
    ) -> None:
        """
        Initializes the chatbot graph with the provided ModelManager and EmbeddingManager.

        Args:
            model_manager (ModelManager): The model manager responsible for interacting with the LLM.
            embedding_manager (EmbeddingManager): The embedding manager responsible for managing local and web search embeddings.
        """
        logger.info(
            "Initializing GraphInitializer with model and embedding managers."
        )  # Log the initialization

        # Private attributes
        self._model_manager: ModelManager = model_manager
        self._embedding_manager: EmbeddingManager = embedding_manager
        self._graph: StateGraph

    # --- Main flow methods ---
    def parse_input(self, state: InputState) -> TranslateState:
        """
        Converts the input into a HumanMessage and encapsulates it in TranslateState.
        """
        question_message = HumanMessage(content=state["question"])
        return TranslateState(question=question_message)

    def translate_and_optimize_question(self, state: TranslateState) -> JsonState:
        """
        Uses the LLM to translate and optimize the question, returning improved_question as MessageLikeRepresentation in JsonState.
        """
        question = state["question"].content  # type: ignore
        prompt = TRANSLATE_OPTIMIZE_QUESTION_PROMPT.format(question=question)
        improved_question = self._model_manager.flash_llm.invoke(prompt).content  # type: ignore
        improved_message = HumanMessage(content=improved_question)
        return JsonState(improved_question=improved_message)

    def extract_json(self, text: str) -> dict[str, object] | None:
        """
        Extracts the first JSON object found in a string and parses it.

        Args:
            text (str): The input string potentially containing a JSON object.
        Returns:
            dict | None: The parsed JSON object if found and valid, otherwise None.
        """
        match = re.search(r"\{[\s\S]*?\}", text)
        if match:
            json_str = match.group(0)
            try:
                return json.loads(json_str)
            except Exception:
                pass
        return None

    def parse_improved_question(self, state: JsonState) -> SearchState:
        """
        Parses the improved_question field from the state, extracting the language and question fields from a JSON string.
        Handles malformed or missing JSON, falling back to the raw string if needed.

        Args:
            state (JsonState): The state containing the improved_question as a MessageLikeRepresentation.
        Returns:
            SearchState: The parsed question as a HumanMessage, with empty context lists.
        """
        improved_question_msg: MessageLikeRepresentation = state.get(
            "improved_question", ""
        )
        improved_question: str = getattr(
            improved_question_msg, "content", str(improved_question_msg)
        )
        parsed: dict[str, object] | None = self.extract_json(improved_question)

        language: str = ""
        improved_question_text: str = ""

        # Check if the JSON was parsed successfully
        if parsed is None:
            logger.error(
                f"Error parsing improved_question JSON. Raw content: {improved_question}"
            )
            improved_question_text = improved_question
            language = "en"  # Default si no se puede extraer
        else:
            language = str(parsed.get("language", "en"))
            improved_question_text = str(parsed.get("question", "")).strip()

        improved_message: HumanMessage = HumanMessage(content=improved_question_text)
        return SearchState(
            question=improved_message,
            local_context=[],
            web_context=[],
            language=language,
        )

    def search_local(self, state: SearchState) -> GenerationState:
        """
        Searches local documents for relevant context based on the user's question.

        Args:
            state (State): The current state containing the user's question.

        Returns:
            dict: A dictionary containing the local search results added to the local context.
        """
        question = state["question"].content  # type: ignore

        local_docs = self._embedding_manager.query_local_embeddings(
            query=question, k=K_LOCAL_SEARCH  # type: ignore
        )
        return {"local_context": local_docs}  # type: ignore

    def search_web(self, state: SearchState) -> GenerationState:
        """
        Searches web documents for relevant context based on the user's question.

        Args:
            state (State): The current state containing the user's question.

        Returns:
            dict: A dictionary containing the web search results added to the web context.
        """
        question = state["question"].content  # type: ignore

        web_docs = self._embedding_manager.query_web_embeddings(
            query=question, k=K_WEB_SEARCH  # type: ignore
        )
        return {"web_context": web_docs}  # type: ignore

    def generate_answer(self, state: GenerationState) -> SummarizationState:
        """
        Generates a response to the user's question using the language model, incorporating the relevant context and any available summary.

        This function constructs a system message that includes the current context, the user's question, and optionally the previous conversation summary.
        It then invokes the language model to generate a response based on this information.

        Args:
            state (State): The current state containing the user's question, context, and potentially a summary of prior conversation.

        Returns:
            dict: A dictionary containing the generated response as a list of messages. The key 'messages' contains the response from the model.
        """
        question = state["question"].content  # type: ignore
        local_context = state["local_context"]
        web_context = state["web_context"]
        summary = state.get("summary", "")
        messages = state["messages"]
        language = state.get("language", "en")

        # Log to verify the context and messages before invocation
        logger.debug(f"Generating answer for question: {question}")
        logger.debug(f"Local context before invocation: {len(local_context)}")
        logger.debug(f"Web context before invocation: {len(web_context)}")
        logger.debug(f"Messages before invocation: {len(messages)}")

        # Prepare system messages based on the context and question
        system_messages: List[BaseMessage] = []

        # Combine local and web context
        combined_context = local_context + web_context

        # Append the context and question to the system message
        system_messages.append(
            SystemMessage(
                content=ANSWER_PROMPT.format(
                    context=combined_context, question=question, language=language
                )
            )
        )

        # If a summary exists, append it to the system message
        if summary:
            system_messages.append(
                SystemMessage(content=SUMMARY_PROMPT.format(summary=summary))
            )

        # Append recent messages to the system message
        if messages:
            system_messages.append(
                SystemMessage(content=RECENT_MESSAGES_PROMPT.format(messages=messages))
            )

        # Add the user question to the message history
        question_message = HumanMessage(content=question)

        # Add an instruction to the model to start answering
        system_messages.append(HumanMessage(content=question))

        logger.debug(f"System messages before invoking model: {len(system_messages)}")

        # Invoke the model with the constructed system messages
        response = self._model_manager.llm.invoke(system_messages)  # type: ignore

        return {"messages": [question_message, response], "answer": response, "documents": combined_context}  # type: ignore

    def summarize_conversation(
        self,
        state: SummarizationState,
    ) -> Dict[str, Union[str, List[RemoveMessage]]]:
        """
        Summarizes the ongoing conversation based on the stored messages and provides a response for summarization.

        This function uses the accumulated conversation history to generate a summary of the interaction.
        It invokes the language model with the conversation summary prompt, appends a summarization instruction, and retrieves the summary from the model.

        Additionally, the function identifies and deletes older messages in the conversation history to maintain context and prevent overloading the model with too much information.

        Args:
            state (State): The current state containing the conversation history (messages) and any existing summary.

        Returns:
            dict: A dictionary containing the conversation summary and a list of messages to delete from the history.
                The 'summary' key contains the generated summary, and the 'messages' key contains the messages to remove.
        """
        summary = state.get("summary", "")
        messages = state["messages"]

        # Prepare system messages for summarization
        system_messages: List[BaseMessage] = []

        # If there is an existing summary, format it as part of the prompt for summarization
        system_messages.append(
            SystemMessage(
                content=SUMMARIZATION_PROMPT.format(summary=summary, messages=messages)
            )
        )

        # Add an instruction to the model to summarize the conversation
        system_messages.append(HumanMessage(content="Summarize the conversation."))

        # Invoke the model with the constructed summarization prompt
        response = self._model_manager.flash_llm.invoke(system_messages)  # type: ignore

        # Identify old messages to remove from the conversation history
        delete_messages: List[RemoveMessage] = [
            RemoveMessage(id=m.id)
            for m in state["messages"][:-2]  # Keep the last two messages
            if m.id is not None
        ]
        return {"summary": response.content, "messages": delete_messages}  # type: ignore

    def should_continue(self, state: SummarizationState, message_threshold: int = 6):
        """
        Determines whether to continue the conversation or summarize it based on the number of messages.

        Args:
            state (State): The current state of the conversation containing all the messages.
            message_threshold (int, optional): The threshold after which summarization should occur. Default is 6.

        Returns:
            Union[str, dict]: The next action, either to continue the conversation or summarize it.
        """
        messages = state["messages"]

        # Check if the conversation exceeds the threshold for summarization
        if len(messages) > message_threshold:
            logger.debug(
                f"Conversation length exceeds {message_threshold} messages. Initiating summarization."
            )
            return "summarize_conversation"
        else:
            return END

    def parse_output(self, state: SummarizationState) -> OutputState:
        """
        Extracts only the answer from the state and returns it as output.

        Args:
            state (State): The current state containing the generated answer.

        Returns:
            OutputState: A dictionary containing only the answer.
        """
        return OutputState(answer=state["answer"].content, documents=state["documents"])  # type: ignore

    # --- Private subgraphs ---
    def _create_translate_subgraph(self) -> None:
        """
        Creates and compiles the subgraph for translation and optimization of the question.
        """
        logger.info("Creating subgraph for question translation/optimization.")
        translate_graph: StateGraph = StateGraph(
            input=TranslateState, output=SearchState
        )
        # Add nodes for translation and optimization
        translate_graph.add_node("translate_and_optimize_question", self.translate_and_optimize_question)  # type: ignore
        translate_graph.add_node("parse_improved_question", self.parse_improved_question)  # type: ignore

        # Define edges for the translation subgraph
        translate_graph.add_edge(START, "translate_and_optimize_question")
        translate_graph.add_edge(
            "translate_and_optimize_question", "parse_improved_question"
        )
        translate_graph.add_edge("parse_improved_question", END)

        # Compile the translation subgraph
        self._translate_subgraph: StateGraph = translate_graph.compile()  # type: ignore
        logger.info("Translate/optimize subgraph created and compiled.")

    def _create_search_subgraph(self) -> None:
        """
        Creates and compiles the search subgraph for local and web searches.
        """
        logger.info("Creating subgraph for local and web search.")
        search_graph: StateGraph = StateGraph(input=SearchState, output=GenerationState)

        # Add nodes for local and web search
        search_graph.add_node("search_local", self.search_local)  # type: ignore
        search_graph.add_node("search_web", self.search_web)  # type: ignore

        # Define edges for the search subgraph
        search_graph.add_edge(START, "search_local")
        search_graph.add_edge(START, "search_web")
        search_graph.add_edge("search_local", END)
        search_graph.add_edge("search_web", END)

        # Compile the search subgraph
        self._search_subgraph: StateGraph = search_graph.compile()  # type: ignore
        logger.info("Search subgraph created and compiled.")

    def _create_llm_subgraph(self) -> None:
        """
        Creates and compiles the LLM invocation subgraph.
        """
        logger.info("Creating subgraph for LLM invocation.")
        llm_graph: StateGraph = StateGraph(
            input=GenerationState, output=SummarizationState
        )

        # Add nodes for generating answers and summarizing conversation
        llm_graph.add_node("generate_answer", self.generate_answer)  # type: ignore
        llm_graph.add_node("summarize_conversation", self.summarize_conversation)  # type: ignore

        # Define edges for the LLM subgraph
        llm_graph.add_edge(START, "generate_answer")
        llm_graph.add_conditional_edges(
            "generate_answer",
            self.should_continue,
            {
                "summarize_conversation": "summarize_conversation",
                END: END,
            },
        )
        llm_graph.add_edge("summarize_conversation", END)

        # Compile the LLM subgraph
        self._llm_subgraph: StateGraph = llm_graph.compile()  # type: ignore
        logger.info("LLM subgraph created and compiled.")

    def _create_main_graph(self) -> None:
        """
        Creates and compiles the main chatbot graph.
        """
        logger.info("Building main chatbot graph.")
        chatbot_graph: StateGraph = StateGraph(GenerationState, output=OutputState)

        # Add nodes for parsing input, searching, invoking LLM, and parsing output
        chatbot_graph.add_node("parse_input", self.parse_input)  # type: ignore
        chatbot_graph.add_node("translate", lambda state: self._translate_subgraph.invoke(state))  # type: ignore
        chatbot_graph.add_node("search", lambda state: self._search_subgraph.invoke(state))  # type: ignore
        chatbot_graph.add_node("llm_invocation", lambda state: self._llm_subgraph.invoke(state))  # type: ignore
        chatbot_graph.add_node("parse_output", self.parse_output)  # type: ignore

        # Define edges for the main chatbot graph
        chatbot_graph.add_edge(START, "parse_input")
        chatbot_graph.add_edge("parse_input", "translate")
        chatbot_graph.add_edge("translate", "search")
        chatbot_graph.add_edge("search", "llm_invocation")
        chatbot_graph.add_edge("llm_invocation", "parse_output")
        chatbot_graph.add_edge("parse_output", END)

        # Compile the main chatbot graph with memory saver
        memory: MemorySaver = MemorySaver()
        self.graph = chatbot_graph.compile(checkpointer=memory)  # type: ignore
        logger.info("Main graph created and compiled successfully.")

        # Generate and display the graph image
        # self._generate_graph_image()

    # def _generate_graph_image(self) -> None:
    #     """
    #     Generates and displays an image of the compiled graph. (This function is currently commented out.)
    #     """
    #     from PIL import Image

    #     image_path = "graph_image.png"
    #     with open(image_path, "wb") as f:
    #         f.write(self.graph.get_graph(xray=True).draw_mermaid_png())  # type: ignore

    #     img = Image.open(image_path)
    #     img.show()

    # --- Initialization of the main graph ---
    def build_graph(self) -> None:
        """
        Builds and compiles the chatbot's state graph, integrating search, answer generation, and summarization.
        """
        self._create_translate_subgraph()
        self._create_search_subgraph()
        self._create_llm_subgraph()
        self._create_main_graph()

    # --- Properties ---
    @property
    def graph(self) -> StateGraph:
        """
        Returns the compiled state graph of the chatbot.
        """
        return self._graph

    @graph.setter
    def graph(self, value: StateGraph) -> None:
        """
        Sets the state graph for the chatbot.

        Args:
            value (StateGraph): The compiled state graph to be set.
        """
        self._graph = value
