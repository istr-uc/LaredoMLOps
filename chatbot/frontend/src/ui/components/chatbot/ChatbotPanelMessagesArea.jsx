// ChatbotPanelMessagesArea.jsx
// ---------------------------------------------
// This component renders the scrollable area containing all chatbot messages.
// It automatically scrolls to the bottom when new messages arrive or loading state changes.

import MessageList from "@/ui/components/message/MessageList.jsx";
import useAutoScroll from "@/core/hooks/useScrollToBottom.js";

/**
 * ChatbotPanelMessagesArea
 *
 * Provides a scrollable container for chatbot messages and ensures the view
 * auto-scrolls to the latest message or loading indicator.
 * @param {{ messages: Array<any>, isLoading: boolean }} props
 * @param {Object} props
 * @param {Array<Object>} props.messages - Array of message objects to display.
 * @param {boolean} props.isLoading - Whether a message is currently being sent/received.
 * @returns {React.ReactElement}
 */
function ChatbotPanelMessagesArea({ messages, isLoading }) {
  // Detect the last message object (for scroll logic)
  const lastMessage =
    messages.length > 0 ? messages[messages.length - 1] : undefined;
  // Use the last message's role and content as dependencies for the scroll hook.
  // This ensures the scroll updates not only on new messages, but also when the assistant streams content.
  const scrollContentRef = useAutoScroll(
    [
      messages.length, // triggers scroll on new message
      isLoading, // triggers scroll on loading state change
      lastMessage?.role, // triggers scroll if the last message changes role (user/assistant)
      lastMessage?.content, // triggers scroll if the last message's content changes (important for streaming)
    ],
    lastMessage?.role,
  ); // pass the last message's role for scroll direction logic

  return (
    <div
      className="flex-1 overflow-auto overflow-y-auto overflow-x-hidden pr-3"
      ref={scrollContentRef}
    >
      {/* Render the list of chat messages and loading indicator if needed */}
      <MessageList messages={messages} isLoading={isLoading} />
    </div>
  );
}

export default ChatbotPanelMessagesArea;
