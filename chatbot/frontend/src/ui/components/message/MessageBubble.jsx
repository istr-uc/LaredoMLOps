// MessageBubble.jsx
// -----------------------------------------------------------------------------------------------
// Renders a single chat message bubble for either the user or assistant, including error states.
// Uses MessageError for errors and MessageBubbleContent for message content.

import MessageError from "@/ui/components/message/MessageError.jsx";
import Markdown from "react-markdown";

// Common background and shadow for all message bubbles
const SHADOW_CHAT = "bg-gray shadow-chatbot";
// Common bubble shape, padding, and text color (text-chat-white)
const COMMON_STYLE = "text-chat-white break-words px-5 py-3 rounded-3xl";

/**
 * MessageBubble Component
 *
 * Renders a chat message bubble for either the user or assistant.
 *
 * @component
 * @param {Object} props - Component props
 * @param {"user"|"assistant"} props.role - The role of the message sender
 * @param {string} props.content - The message content
 * @param {boolean} props.error - Whether the message is an error
 * @param {boolean} props.animate - Whether to apply the fade animation
 * @returns {React.ReactElement}
 */
const MessageBubble = ({ role, content, error, animate }) => {
  if (error) return <MessageError />;

  if (role === "user") {
    return (
      <div
        className={`${SHADOW_CHAT} ${COMMON_STYLE} max-w-[70%] w-fit ml-auto`}
        style={{ display: 'flex', justifyContent: 'flex-end' }}
      >
        <span className="block whitespace-pre-line text-left w-full" style={{ textAlign: 'left' }}>{content}</span>
      </div>
    );
  }

  // assistant
  return (
    <div
      className={`markdown-container ${COMMON_STYLE}${animate ? " animate-assistant-message" : ""} text-left`}
    >
      <Markdown>{content}</Markdown>
    </div>
  );
};

export default MessageBubble;
