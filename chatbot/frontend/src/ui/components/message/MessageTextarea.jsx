// MessageTextarea.jsx - Modularized and documented textarea for chat input
// ---------------------------------------------------------------
// This component renders a multi-line textarea for chat messages.
// It uses a custom hook to autosize the textarea as the user types.

import React from "react";
import useAutosizeTextarea from "@/core/hooks/useAutosizeTextarea.js";

/**
 * MessageTextarea Component
 *
 * Renders a multi-line textarea for chat input, with autosizing and accessibility features.
 *
 * @param {Object} props - Component props
 * @param {string} props.value - The current value of the textarea
 * @param {(e: React.ChangeEvent<HTMLTextAreaElement>) => void} props.onChange - Handler for textarea value changes
 * @param {(e: React.KeyboardEvent<HTMLTextAreaElement>) => void} props.onKeyDown - Handler for keydown events (e.g., Enter to send)
 * @param {React.RefObject<HTMLTextAreaElement>} [props.inputRef] - Optional ref for external focus control
 * @param {boolean} [props.isLoading] - If true, disables the textarea
 * @returns {React.ReactElement}
 */
function MessageTextarea({ value, onChange, onKeyDown, isLoading }) {
  // Custom hook to autosize the textarea as the user types
  const textareaRef = useAutosizeTextarea(value);

  return (
    <textarea
      // Use the provided ref if available, otherwise use the autosize ref
      ref={textareaRef}
      className="placeholder-light-blue/50 text-chat-white/100 w-full h-full flex items-center bg-transparent resize-none focus:outline-none max-h-32"
      rows={1} // Start with a single row, autosize will expand as needed
      value={value}
      onChange={onChange}
      onKeyDown={onKeyDown}
      placeholder="Type your message here..."
      aria-label="Chat message input"
      spellCheck={true}
      autoComplete="off"
      autoCorrect="on"
    />
  );
}

export default MessageTextarea;
