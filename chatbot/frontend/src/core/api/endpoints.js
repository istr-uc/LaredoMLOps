// Endpoint utility for chatbot API

/**
 * Retrieves the base URL for the API from environment variables.
 * @param {string} apiUrl - The base API URL.
 * @returns {string} The base API URL.
 * @throws {Error} If the API URL is not set.
 */
export const getApiBaseUrl = (apiUrl) => {
  if (!apiUrl) throw new Error("API base URL must be provided as a parameter.");
  return apiUrl;
};

/**
 * Constructs the chatbot endpoint URL.
 * @param {string} path - The API path (e.g., '/chatbot' or '/chatbot/stream').
 * @param {string} apiUrl - The base API URL.
 * @returns {string} The chatbot endpoint URL.
 */
export const getChatbotEndpoint = (path, apiUrl) =>
  `${getApiBaseUrl(apiUrl)}${path}`;
