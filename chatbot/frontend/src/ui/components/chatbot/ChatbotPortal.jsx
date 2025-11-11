// ChatbotPortal.jsx
// -----------------------------------------------------------------------------
// Floating chatbot widget controller: manages the open/close button, panel visibility,
// pinning, focus, and click-outside logic. All animation logic is modularized.
// -----------------------------------------------------------------------------

import { useState, useRef } from "react";
import ChatbotPanel from "./ChatbotPanel.jsx";
import ChatbotPanelButton from "./ChatbotPanelButton.jsx";
import useChatbotConversation from "@/core/chatbot/useChatbotConversation.js";
import useChatbotAnimation from "@/core/chatbot/useChatbotAnimation.js";
import useClickOutside from "@/core/hooks/useClickOutside.js";
import useFocusOnOpen from "@/core/hooks/useFocusOnOpen.js";

// Change this to false to use block mode (classic, non-streaming)
const USE_STREAM = true;

/**
 * ChatbotPortal
 *
 * Main controller for the floating chatbot widget.
 * - Shows a floating button when closed.
 * - Shows the chatbot panel when open.
 * - Handles pinning, focus, and click-outside-to-close.
 * - All animation state is managed by useChatbotButtonAnimation.
 *
 * @param {{ apiUrl: string }} props
 */
function ChatbotPortal({ apiUrl }) {
  // Animation and panel state (from custom hook)
  const {
    isOpen,
    showButton,
    buttonAnimation,
    panelAnimation,
    handlePanelOpen,
    handlePanelClose,
    isPanelAnimatingOut,
  } = useChatbotAnimation();

  // Pinning state for keeping the panel open
  const [pinned, setPinned] = useState(false);

  // Refs for input focus and click-outside detection
  const inputRef = useRef(null);
  const containerRef = useRef(null);

  // Chatbot conversation state and actions
  const {
    messages,
    isLoading,
    sendMessageBlock,
    sendMessageStream,
    clearChat,
  } = useChatbotConversation(apiUrl);

  // Close panel on outside click (unless pinned or animating out)
  useClickOutside(
    containerRef,
    handlePanelClose,
    isOpen && !pinned && !isPanelAnimatingOut
  );
  // Focus input when panel opens
  useFocusOnOpen(isOpen && !isPanelAnimatingOut, inputRef);

  // Toggle pin state handler
  const handlePin = () => setPinned((p) => !p);
  // Clear chat handler
  const handleClearChat = () => clearChat();

  // Render chatbot panel if open
  if (isOpen) {
    return (
      <div
        className={`fixed bottom-5 right-5 z-50 chatbot-portal-panel ${panelAnimation}`}
      >
        <ChatbotPanel
          messages={messages}
          isLoading={isLoading}
          sendMessage={USE_STREAM ? sendMessageStream : sendMessageBlock}
          pinned={pinned}
          onPin={handlePin}
          onClear={handleClearChat}
          onClose={handlePanelClose}
          inputRef={inputRef}
          containerRef={containerRef}
        />
      </div>
    );
  }

  // Render floating button if panel is closed and button should be shown
  if (showButton) {
    return (
      <div
        className={`fixed bottom-5 right-5 z-50 chatbot-portal-button ${buttonAnimation}`}
      >
        <ChatbotPanelButton onClick={handlePanelOpen} />
      </div>
    );
  }

  // Render nothing if neither panel nor button should be shown
  return null;
}

export default ChatbotPortal;
