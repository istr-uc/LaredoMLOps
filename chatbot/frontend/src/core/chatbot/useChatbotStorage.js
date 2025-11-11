// useChatbotStorage.js - Handles localStorage for chatbot messages
// ---------------------------------------------------------------

// Key used for storing messages in localStorage
const STORAGE_KEY = "chatbot-messages";

/**
 * Loads messages from localStorage.
 * @returns {Array<any>} Array of chat messages, or [] if none found or error.
 */
export function loadMessages() {
  try {
    // Retrieve the stored messages string
    const stored = localStorage.getItem(STORAGE_KEY);
    // Parse and return messages if found, else return empty array
    return stored ? JSON.parse(stored) : [];
  } catch {
    // On error, return empty array
    return [];
  }
}

/**
 * Saves messages to localStorage.
 * @param {Array<any>} messages - Array of chat messages to store.
 */
export function saveMessages(messages) {
  try {
    // Convert messages array to JSON and store
    localStorage.setItem(STORAGE_KEY, JSON.stringify(messages));
  } catch {
    // Ignore storage errors (e.g., quota exceeded)
  }
}

/**
 * Clears all stored chat messages from localStorage.
 */
export function clearStoredMessages() {
  try {
    // Remove the messages key from storage
    localStorage.removeItem(STORAGE_KEY);
  } catch {
    // Ignore storage errors
  }
}
