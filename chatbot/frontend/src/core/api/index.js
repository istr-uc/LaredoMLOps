// Main API function for chatbot backend
import { getChatbotEndpoint } from "./endpoints.js";
import {
  throwNetworkError,
  throwInvalidJsonError,
  throwApiError,
  throwInvalidResponseFormat,
} from "./errors.js";

/**
 * Sends a message to the chatbot backend and returns the assistant's response.
 * @param {string} userMessage - The user's message to send.
 * @param {string} apiUrl - The base API URL.
 * @returns {Promise<string>} The assistant's response.
 * @throws {Error} If the API call fails or the response is invalid.
 */
export const fetchAssistantResponse = async (userMessage, apiUrl) => {
  // Validate input
  if (typeof userMessage !== "string" || !userMessage.trim()) {
    throw new Error("User message must be a non-empty string.");
  }

  // Prepare endpoint and payload
  const endpoint = getChatbotEndpoint("/chatbot", apiUrl);
  const payload = JSON.stringify({ question: userMessage.trim() });

  let response = undefined;
  try {
    // Send POST request to the chatbot API
    response = await fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: payload,
    });
  } catch (error) {
    throwNetworkError(
      error instanceof Error ? error : new Error(String(error)),
    );
  }

  let data;
  try {
    if (!response) throw new Error("No response received from API.");
    // Parse JSON response from the API
    data = await response.json();
  } catch (error) {
    throwInvalidJsonError(
      error instanceof Error ? error : new Error(String(error)),
    );
  }

  // Handle non-OK HTTP responses
  if (!response || !response.ok) {
    throwApiError(response || new Response(), data);
  }

  // Validate the structure of the API response
  if (!data || typeof data.answer !== "string") {
    throwInvalidResponseFormat();
  }

  // Return the assistant's answer
  return data.answer;
};

/**
 * Streams the assistant's response in real time using a custom chunk delimiter.
 * @param {string} userMessage - The user's message to send to the chatbot.
 * @param {(chunk: string) => void} onChunk - Callback for each processed chunk of the assistant's response.
 * @param {AbortSignal} [signal] - Optional AbortSignal to allow cancellation.
 * @param {string} apiUrl - The base API URL.
 * @returns {Promise<void>} Resolves when the stream ends or is aborted.
 * @throws {Error} If the network or stream fails.
 */
export const streamAssistantResponse = async (
  userMessage,
  onChunk,
  apiUrl,
  signal,
) => {
  // Validate input
  if (typeof userMessage !== "string" || !userMessage.trim()) {
    throw new Error("User message must be a non-empty string.");
  }

  // Build the streaming endpoint URL and payload
  const endpoint = getChatbotEndpoint("/chatbot/stream", apiUrl);
  const payload = JSON.stringify({ question: userMessage.trim() });

  let response;
  try {
    // Send POST request to the streaming endpoint
    response = await fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: payload,
      signal,
    });
  } catch (error) {
    if (signal?.aborted) return; // Request was aborted by the caller
    throw new Error("Network error while connecting to streaming endpoint.");
  }

  if (!response.ok || !response.body) {
    throw new Error("Failed to connect to streaming endpoint.");
  }

  // Prepare to read the response as a stream
  const reader = response.body.getReader();
  const decoder = new TextDecoder("utf-8");
  let buffer = "";

  try {
    while (true) {
      // Read a chunk from the stream
      const { value, done } = await reader.read();
      if (done) break;
      // Decode the chunk and append to buffer
      const decoded = decoder.decode(value, { stream: true });
      buffer += decoded;
      // Split buffer by the custom delimiter
      let splitChunks = buffer.split("<END_OF_CHUNK>");
      // All except the last are complete chunks
      for (let i = 0; i < splitChunks.length - 1; i++) {
        let chunk = splitChunks[i];
        // Remove the first 6 and last 2 characters if chunk is long enough
        // (for legacy compatibility with previous SSE format)
        if (chunk.length > 8) {
          chunk = chunk.slice(6, -2);
        }
        if (chunk) onChunk(chunk);
      }
      // The last part may be incomplete, keep it in buffer
      buffer = splitChunks[splitChunks.length - 1];
    }
    // If anything remains in buffer at the end, process it as a final chunk
    if (buffer.length > 8) {
      const chunk = buffer.slice(6, -2);
      if (chunk) onChunk(chunk);
    }
  } finally {
    reader.releaseLock();
  }
};
