"""
api.py - Main Flask API for the chatbot backend
------------------------------------------------
Defines endpoints for synchronous and streaming chatbot responses.
Includes CORS support and helper functions for validation and error handling.
"""

from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from src.api.chatbot_service import ChatbotService
from src.config.config_init import FLASK_PORT, FLASK_DEBUG
import asyncio
from typing import Any, Optional, Tuple


def _get_question_from_request() -> Tuple[Optional[str], Any, Optional[int]]:
    """
    Extracts and validates the 'question' field from the incoming JSON request.
    Returns (question, error_response, status_code).
    """
    data = request.json
    if not data or "question" not in data or not isinstance(data["question"], str):
        return None, jsonify({"error": "A valid 'question' (string) is required"}), 400
    return data["question"], None, None


def _handle_exception(e: Exception) -> Tuple[Any, int]:
    """
    Returns a JSON error response for any exception.
    """
    return jsonify({"error": str(e)}), 500


def create_app() -> Flask:
    """
    Creates and configures the Flask app, including all chatbot endpoints.
    """
    app = Flask(__name__)
    CORS(app)  # Enable CORS globally

    chatbot_service = ChatbotService()

    @app.route("/chatbot", methods=["POST"])
    async def chatbot_endpoint() -> tuple[Any, int]:  # type: ignore
        """
        Synchronous endpoint: returns the full chatbot response as JSON.
        """
        try:
            question, error_response, status = _get_question_from_request()
            if error_response:
                return error_response, status or 400
            if question is None:
                return (
                    jsonify({"error": "A valid 'question' (string) is required"}),
                    400,
                )
            response = await chatbot_service.generate_response(question)
            return jsonify({"answer": response}), 200
        except Exception as e:
            return _handle_exception(e)

    @app.route("/chatbot/stream", methods=["POST"])
    def chatbot_stream_endpoint() -> Any:  # type: ignore
        """
        Streaming endpoint: returns the chatbot response in real time
        Uses SSE but with final delimiter <END_OF_CHUNK> for compatibility with markdown.
        """
        try:
            question, error_response, status = _get_question_from_request()
            if error_response:
                return error_response, status
            if question is None:
                return (
                    jsonify({"error": "A valid 'question' (string) is required"}),
                    400,
                )

            # Async generator yielding raw chunks from the chatbot service
            async def async_event_stream():
                async for chunk in chatbot_service.generate_response_stream(question):
                    yield chunk

            # Sync generator bridging async generator to Flask's streaming response
            def sync_event_stream():
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                agen = async_event_stream()
                try:
                    while True:
                        chunk = loop.run_until_complete(agen.__anext__())
                        yield chunk  # Each chunk ends with <END_OF_CHUNK>
                except StopAsyncIteration:
                    pass
                finally:
                    loop.close()

            return Response(sync_event_stream(), mimetype="text/event-stream")
        except Exception as e:
            return _handle_exception(e)

    @app.route("/hello", methods=["GET"])
    def saludo() -> tuple[Any, int]:  # type: ignore
        """
        Simple health check endpoint.
        """
        return jsonify({"mensaje": "Hello, I'm working", "version": "1.0"}), 200

    return app


# Entrypoint for running the Flask application
app = create_app()

if __name__ == "__main__":
    app.run(port=FLASK_PORT, debug=FLASK_DEBUG)
