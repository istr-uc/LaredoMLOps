import chatIcon from "@/assets/images/icon-chat.svg";

// Standardized button size using Tailwind's w-16 h-16
const BASE_BTN_CLASS =
  "flex items-center justify-center w-16 h-16 rounded-3xl hover:animate-chatbot-pulse-shadow-btn";
const FROSTED_GLASS_PBUTTON = "backdrop-blur-lg";
const SHADOW_BUTTON = "bg-dark-gray/80 shadow-chatbot";

/**
 * ChatbotButton - A reusable floating action button for the chatbot UI.
 *
 * Props:
 * @param {Object} props - Component props
 * @param {string} [props.className] - Additional Tailwind or custom classes for styling
 * @param {string} props.icon - Path to the icon image (SVG or other)
 * @param {(e: React.MouseEvent<HTMLButtonElement>) => void} props.onClick - Handler for button click events
 * @param {string} props.title - Tooltip text for accessibility and hover
 * @param {string} [props.ariaLabel] - Optional aria-label for screen readers (defaults to title)
 *
 * @returns {React.ReactElement} A styled button with an icon, accessible and keyboard-friendly
 */
function ChatbotButton({ className = "", icon, onClick, title, ariaLabel }) {
  // Render a button with icon and accessibility features
  return (
    <button
      type="button"
      onClick={onClick}
      className={`${BASE_BTN_CLASS} ${SHADOW_BUTTON}  ${FROSTED_GLASS_PBUTTON} ${className}`}
      title={title}
      aria-label={ariaLabel || title}
    >
      {/* Icon image for the button */}
      <img src={icon} className="w-8 h-8" alt="Chat icon" draggable={false} />
    </button>
  );
}

/**
 * ChatbotPanelButton
 *
 * Floating button to open the chatbot panel.
 * Receives animation and extra styles through the `className` prop.
 *
 * Props:
 * @param {Object} props - Component props
 * @param {(e: React.MouseEvent<HTMLButtonElement>) => void} props.onClick - Action when clicking (opens the panel)
 * @param {string} [props.className] - Extra classes for animation or styles
 */
const ChatbotPanelButton = ({ onClick, className = "" }) => {
  // Renders the floating action button for the chatbot, with optional animation classes
  return (
    <ChatbotButton
      onClick={onClick}
      icon={chatIcon}
      title="Open chat"
      className={className}
    />
  );
};

export default ChatbotPanelButton;
