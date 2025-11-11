// MessageError.jsx - Error indicator for chat assistant
// -----------------------------------------------------
// Shows an error icon and message when the assistant fails to generate a response.

import errorIcon from "@/assets/images/icon-error.svg";

/**
 * MessageError Component
 *
 * Displays an error icon and a message when the assistant fails to respond.
 *
 * @returns {React.ReactElement}
 */
function MessageError() {
  return (
    <div className="gap-2 flex items-center">
      <img className="h-5 w-5" src={errorIcon} alt="error" />
      <span className="text-error-red">Error generating response.</span>
    </div>
  );
}

export default MessageError;
