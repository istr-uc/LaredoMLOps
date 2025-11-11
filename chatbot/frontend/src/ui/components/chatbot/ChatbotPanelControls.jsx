// ChatbotControls.jsx - Modularized control buttons for ChatbotButton
import pinIcon from "@/assets/images/icon-pin.svg";
import trashIcon from "@/assets/images/icon-trash.svg";
import closeIcon from "@/assets/images/icon-close.svg";
import BrandName from "./BrandName.jsx";

// Shared button styles
const BASE_BTN_CLASS = `flex items-center justify-center w-8 h-8 rounded-3xl hover:animate-chatbot-pulse-shadow-btn`;

// Shared shadow style
const SHADOW_BUTTON = "bg-gray shadow-chatbot";

/**
 * Generic control button for the chatbot panel.
 * @param {Object} props
 * @param {string} [props.className] - Extra classes for the button
 * @param {string} props.icon - Icon source
 * @param {(e: React.MouseEvent<HTMLButtonElement>) => void} props.onClick - Click handler
 * @param {string} [props.title] - Title attribute for the button
 */
function ChatbotControlButton({ className = "", icon, onClick, title }) {
  return (
    <button
      onClick={onClick}
      className={`${BASE_BTN_CLASS} ${SHADOW_BUTTON} ${className}`}
      title={title}
    >
      <img src={icon} className="w-5 h-5" />
    </button>
  );
}

/**
 * ChatbotPanelControls
 * Modularized control panel for chatbot actions.
 * @param {{ pinned: boolean, onPin: (e: React.MouseEvent<HTMLButtonElement>) => void, onClear: (e: React.MouseEvent<HTMLButtonElement>) => void, onClose: (e: React.MouseEvent<HTMLButtonElement>) => void }} props
 */
function ChatbotPanelControls({ pinned, onPin, onClear, onClose }) {
  return (
    <div className="flex items-center justify-end gap-2">
      {/* BrandName to the far left */}
      <BrandName />
      <div className="flex-1" />
      {/* Control buttons aligned right */}
      <ChatbotControlButton
        onClick={onPin}
        className={`chatbot-pin-btn${pinned ? " pinned" : ""}`}
        icon={pinIcon}
        title={pinned ? "Unpin chat" : "Pin chat"}
      />
      <ChatbotControlButton
        onClick={onClear}
        className=""
        icon={trashIcon}
        title="Clear chat"
      />
      <ChatbotControlButton
        onClick={onClose}
        className=""
        icon={closeIcon}
        title="Close chat"
      />
    </div>
  );
}

export default ChatbotPanelControls;
