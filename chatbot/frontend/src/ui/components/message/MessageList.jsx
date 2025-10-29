// MessageList.jsx - Chat message list for the chatbot UI
// ------------------------------------------------------
// Renders all chat messages and a loading indicator when the assistant is thinking.
// MessageList only maps messages to MessageBubble; role logic is handled in MessageBubble.

import MessageBubble from "./MessageBubble.jsx";
import MessageLoading from "./MessageLoading.jsx";

/**
 * @typedef {Object} Message
 * @property {"user"|"assistant"} role - Who sent the message
 * @property {string} [content] - The message text
 * @property {boolean} [error] - If true, message is an error (assistant only)
 */

/**
 * MessageList Component
 *
 * Renders a vertical list of chat messages. If the assistant is generating a response
 * (isLoading), shows a loading indicator at the end of the list.
 *
 * - The last message is always from the assistant when isLoading is true.
 * - Only that message receives the fade-in animation for new chunks.
 *
 * @param {{ messages: Message[], isLoading: boolean }} props
 *   messages: Array of chat messages (user and assistant)
 *   isLoading: True if the assistant is currently generating a response
 * @returns {React.ReactElement}
 */
function MessageList({ messages, isLoading }) {
  // The index of the last message (always assistant when isLoading)
  const lastIdx = messages.length - 1;

  return (
    <div className="flex flex-col gap-2">
      {/* Render each chat message as a bubble. Only the last assistant message animates when loading. */}
      {messages.map((m, i) => (
        <MessageBubble
          key={i}
          role={m.role}
          content={m.content || ""}
          error={!!m.error}
          // Apply fade only to the last message when isLoading
          animate={isLoading && i === lastIdx}
        />
      ))}
      {/* Loading indicator: visible only when assistant is generating a response */}
      <div
        style={{ minHeight: "2.5em" }}
        aria-hidden={!isLoading}
        className={isLoading ? "" : "opacity-0 pointer-events-none select-none"}
      >
        <MessageLoading />
      </div>
    </div>
  );
}

export default MessageList;
