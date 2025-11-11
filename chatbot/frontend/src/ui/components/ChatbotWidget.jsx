// Component encapsulated to import the chatbot into the app
import ChatbotPortal from "@/ui/components/chatbot/ChatbotPortal.jsx";
import ShadowRoot from "react-shadow";

import "@/ui/styles/chatbot-widget.css"; // import for building the widget
import chatbotWidgetCss from "../styles/laredocmind.css?raw";

// Allows passing the backend URL as a prop (defaults to localhost)
/**
 * @param {{ apiUrl: string }} props
 * apiUrl is a string URL for the backend API
 */
export const ChatbotWidget = ({ apiUrl = "http://localhost:20000" }) => {
  return (
    <ShadowRoot.div>
      <style>{chatbotWidgetCss}</style>
      <div className="chatbot-widget">
        <ChatbotPortal apiUrl={apiUrl} />
      </div>
    </ShadowRoot.div>
  );
};
