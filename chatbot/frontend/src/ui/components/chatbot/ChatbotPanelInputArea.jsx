// ChatbotPanelInputArea.jsx
// Chatbot input area component

import { useState } from "react";
import MessageInput from "@/ui/components/message/MessageInput.jsx";

/**
 * ChatbotPanelInputArea
 *
 * Renders the chatbot input area and manages the message state.
 *
 * Props:
 * @param {Object} props - Component properties
 * @param {boolean} props.isLoading - Indicates if the chatbot is processing a response
 * @param {function(string):void} props.sendMessage - Function to send the written message
 *
 * @returns {React.ReactElement} The chatbot input area
 */
function ChatbotPanelInputArea({ isLoading, sendMessage }) {
  // Local state for the current message
  const [message, setMessage] = useState("");

  /**
   * Sends the current message if it's not empty
   * Clears the input after sending
   */
  const handleSend = () => {
    if (message.trim()) {
      sendMessage(message);
      setMessage("");
    }
  };

  // Renders the message input component
  return (
    <MessageInput
      newMessage={message} // Current message
      isLoading={isLoading} // Loading state
      setNewMessage={setMessage} // Setter to update the message
      submitNewMessage={handleSend} // Handler to send the message
    />
  );
}

export default ChatbotPanelInputArea;
