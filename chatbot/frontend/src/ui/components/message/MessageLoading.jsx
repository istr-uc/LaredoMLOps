// MessageLoading.jsx - Loading indicator for chat assistant
// --------------------------------------------------------
// Shows a spinner and a loading message when the assistant is thinking.

import SpinnerContainer from "@/ui/components/spinner/SpinnerContainer.jsx";

/**
 * MessageLoading Component
 *
 * Displays a spinner and a loading message while the assistant is generating a response.
 * Used in the chat message list during loading state.
 *
 * @returns {React.ReactElement}
 */
function MessageLoading() {
  return (
    // Container for spinner and loading text
    <div className="gap-2 flex items-center">
      {/* Spinner animation */}
      <SpinnerContainer />
      {/* Loading message text */}
      <span className="text-light-blue animate-pulse">Thinking...</span>
    </div>
  );
}

export default MessageLoading;
