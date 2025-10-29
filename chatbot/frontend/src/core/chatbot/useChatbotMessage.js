// useChatbotMessage.js - Utilities for chatbot message creation
// -------------------------------------------------------------
// Provides helper functions to create user and assistant message objects for the chatbot conversation.

/**
 * Creates a user message object for the chatbot conversation.
 *
 * @param {string} content - The user's message content
 * @returns {{ role: 'user', content: string }} User message object
 */
export function createUserMessage(content) {
  return { role: "user", content };
}

/**
 * Creates an assistant message object for the chatbot conversation.
 *
 * @param {string} content - The assistant's message content
 * @returns {{ role: 'assistant', content: string }} Assistant message object
 */
export function createAssistantMessage(content) {
  return { role: "assistant", content };
}
