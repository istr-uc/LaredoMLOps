// ChatbotPanel.jsx - Floating Chatbot Panel UI
// ---------------------------------------------------------------
// Main floating panel for the chatbot interface. Contains control buttons,
// the chat area (messages or welcome), and the input area for sending messages.

import React from "react";
import ChatbotPanelControls from "./ChatbotPanelControls.jsx";
import ChatbotPanelWelcome from "./ChatbotPanelWelcome.jsx";
import ChatbotPanelMessagesArea from "@/ui/components/chatbot/ChatbotPanelMessagesArea.jsx";
import ChatbotPanelInputArea from "@/ui/components/chatbot/ChatbotPanelInputArea.jsx";
import { useResizablePanel } from "@/core/hooks/useResizablePanel.js";
import ResizeHandle from "./ResizeHandle.jsx";

// Tailwind/utility classes for panel appearance
const SHADOW_PANEL = "bg-dark-gray/80 shadow-chatbot backdrop-blur-lg";

/**
 * ChatbotPanel
 *
 * Floating panel UI for the chatbot. Renders controls, messages/welcome, and input.
 * Handles resizing from the top-left corner using a custom hook and handle.
 *
 * Props:
 * @param {Object} props
 * @param {Array<{role: string, content?: string, error?: boolean}>} props.messages - Chat message history
 * @param {boolean} props.isLoading - Whether the assistant is generating a response
 * @param {(msg: string) => void} props.sendMessage - Function to send a new message
 * @param {boolean} props.pinned - Whether the chat is pinned open
 * @param {() => void} props.onPin - Handler to pin/unpin the chat
 * @param {() => void} props.onClear - Handler to clear the chat history
 * @param {() => void} props.onClose - Handler to close the chat panel
 * @param {React.RefObject<HTMLInputElement>} [props.inputRef] - Ref for focusing the input (optional)
 * @param {React.RefObject<HTMLDivElement>} props.containerRef - Ref for click-outside detection
 */
function ChatbotPanel({
  messages,
  isLoading,
  sendMessage,
  pinned,
  onPin,
  onClear,
  onClose,
  inputRef,
  containerRef,
}) {
  // Get panel style, resize state, and handle event from the custom hook
  const { panelStyle, handleResizeHandleMouseDown } = useResizablePanel({
    containerRef,
  });

  // Decide what to show in the main chat area (welcome or messages)
  const mainContent =
    messages.length > 0 ? (
      <ChatbotPanelMessagesArea messages={messages} isLoading={isLoading} />
    ) : (
      <ChatbotPanelWelcome />
    );

  return (
    <div
      ref={containerRef}
      className={`flex flex-col gap-6 p-6 rounded-3xl ${SHADOW_PANEL}`}
      style={panelStyle}
    >
      {/* Resize handle in the top-left corner */}
      <ResizeHandle onMouseDown={handleResizeHandleMouseDown} />

      {/* Top control buttons: pin, clear, close */}
      <ChatbotPanelControls
        pinned={pinned}
        onPin={onPin}
        onClear={onClear}
        onClose={onClose}
      />
      {/* Main chat area: welcome or messages */}
      {mainContent}
      {/* Input area for sending new messages */}
      <ChatbotPanelInputArea isLoading={isLoading} sendMessage={sendMessage} />
    </div>
  );
}

export default ChatbotPanel;
