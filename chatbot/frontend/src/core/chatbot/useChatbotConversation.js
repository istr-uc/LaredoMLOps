// useChatbotConversation.js - Custom React hook for chatbot state and logic
// -------------------------------------------------------------------------
// Provides all state and actions for the chatbot UI, including message history,
// loading state, persistence, and both block and streaming API communication.

import { useState, useEffect, useCallback } from "react";
import {
  fetchAssistantResponse,
  streamAssistantResponse,
} from "@/core/api/index.js";
import {
  loadMessages,
  saveMessages,
  clearStoredMessages,
} from "./useChatbotStorage.js";
import {
  createUserMessage,
  createAssistantMessage,
} from "./useChatbotMessage.js";

/**
 * @typedef {Object} ChatbotConversationApi
 * @property {Array<{role: string, content: string}>} messages - The chat message history (user and assistant)
 * @property {boolean} isLoading - Whether the assistant is generating a response
 * @property {(userInput: string) => Promise<void>} sendMessageBlock - Sends a user message and fetches the assistant's reply in block mode (classic, non-streaming)
 * @property {(userInput: string) => Promise<void>} sendMessageStream - Sends a user message and fetches the assistant's reply in streaming mode (real-time chunks)
 * @property {() => void} clearChat - Clears the chat history and localStorage
 */

/**
 * useChatbotConversation - Central React hook for chatbot conversation logic.
 *
 * @param {string} apiUrl - The base API URL for the backend.
 * @returns {ChatbotConversationApi} API for chatbot conversation state and actions
 */
function useChatbotConversation(apiUrl) {
  // --- Initialization and State ---

  // On first page load, clear chat history (but not on refresh)
  if (
    typeof window !== "undefined" &&
    !sessionStorage.getItem("chatbot-initialized")
  ) {
    clearStoredMessages();
    sessionStorage.setItem("chatbot-initialized", "true");
  }

  // State: chat messages (array of {role, content, ...}) and loading status
  const [messages, setMessages] = useState(loadMessages); // Load from localStorage
  const [isLoading, setIsLoading] = useState(false); // True while assistant is responding

  // Persist messages to localStorage on every change
  useEffect(() => {
    saveMessages(messages);
  }, [messages]);

  // --- Chat Management Actions ---

  /**
   * Clears the chat history and removes it from localStorage.
   * Use this to reset the conversation.
   */
  const clearChat = useCallback(() => {
    setMessages([]);
    clearStoredMessages();
  }, []);

  // --- Message Sending Modes ---

  /**
   * Sends a user message and fetches the assistant's reply in block mode (classic, non-streaming).
   * The assistant's full response is shown only when complete.
   *
   * @param {string} userInput - The user's message to send
   * @returns {Promise<void>}
   */
  const sendMessageBlock = useCallback(
    /**
     * @param {string} userInput - The user's message to send
     */
    async (userInput) => {
      if (isLoading) return; // Prevent concurrent sends
      const trimmedMessage =
        typeof userInput === "string" ? userInput.trim() : "";
      if (!trimmedMessage) return; // Ignore empty input
      setMessages((prev) => [...prev, createUserMessage(trimmedMessage)]);
      setIsLoading(true);
      try {
        const assistantReply = await fetchAssistantResponse(
          trimmedMessage,
          apiUrl,
        );
        setMessages((prev) => [
          ...prev,
          createAssistantMessage(assistantReply),
        ]);
      } catch {
        setMessages((prev) => [
          ...prev,
          {
            role: "assistant",
            content: "Error generating response.",
            error: true,
          },
        ]);
      } finally {
        setIsLoading(false);
      }
    },
    [isLoading, apiUrl],
  );

  /**
   * Sends a user message and fetches the assistant's reply in streaming mode (real-time chunks).
   * The assistant's message is updated progressively as each chunk arrives.
   *
   * @param {string} userInput - The user's message to send
   * @returns {Promise<void>}
   */
  const sendMessageStream = useCallback(
    /**
     * @param {string} userInput - The user's message to send
     */
    async (userInput) => {
      if (isLoading) return; // Prevent concurrent sends
      const trimmedMessage =
        typeof userInput === "string" ? userInput.trim() : "";
      if (!trimmedMessage) return; // Ignore empty input
      setMessages((prev) => [...prev, createUserMessage(trimmedMessage)]);
      setIsLoading(true);
      // Prepare a mutable assistant message object for progressive update
      let assistantMsg = { role: "assistant", content: "" };
      setMessages((prev) => [...prev, assistantMsg]);
      try {
        await streamAssistantResponse(
          trimmedMessage,
          (chunk) => {
            assistantMsg.content += chunk;
            setMessages((prev) => {
              const updated = [...prev];
              updated[updated.length - 1] = { ...assistantMsg };
              return updated;
            });
          },
          apiUrl,
        );
      } catch {
        setMessages((prev) => [
          ...prev.slice(0, -1),
          {
            role: "assistant",
            content: "Error generating response.",
            error: true,
          },
        ]);
      } finally {
        setIsLoading(false);
      }
    },
    [isLoading, apiUrl],
  );

  // --- Return API ---
  return {
    messages, // Array of chat messages (user and assistant)
    isLoading, // True if assistant is generating a response
    sendMessageBlock, // Send message in block mode (classic)
    sendMessageStream, // Send message in streaming mode (real-time)
    clearChat, // Clear chat history
  };
}

export default useChatbotConversation;
