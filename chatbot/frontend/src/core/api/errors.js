// Error handling utilities for chatbot API

/**
 * Throws a network error with an optional message from the caught error.
 * @param {Error} error - The caught error object.
 * @throws {Error}
 */
export function throwNetworkError(error) {
  throw new Error(
    `Network error: Unable to reach the assistant API. ${error?.message || ""}`,
  );
}

/**
 * Throws an error for invalid JSON responses.
 * @param {Error} error - The caught error object.
 * @throws {Error}
 */
export function throwInvalidJsonError(error) {
  throw new Error(
    `Invalid JSON response from assistant API. ${error?.message || ""}`,
  );
}

/**
 * Throws an error for API responses with error status.
 * @param {Response} response - The fetch response object.
 * @param {{ error?: string }} data - The parsed response data.
 * @throws {Error}
 */
export function throwApiError(response, data) {
  throw new Error(
    data.error || `Error: ${response.status} ${response.statusText}`,
  );
}

/**
 * Throws an error for invalid API response format.
 * @throws {Error}
 */
export function throwInvalidResponseFormat() {
  throw new Error("Invalid response format from assistant API.");
}
