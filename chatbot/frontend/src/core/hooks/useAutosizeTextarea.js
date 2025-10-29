// useAutosizeTextarea.js - Custom React hook for autosizing textareas
// ---------------------------------------------------------------
// Dynamically adjusts the height of a textarea element to fit its content.
// Ensures a seamless multi-line input experience for chat or forms.

import { useRef, useLayoutEffect } from "react";

/**
 * useAutosizeTextarea - Custom React hook
 *
 * Automatically resizes a textarea to fit its content whenever the value changes.
 *
 * @param {string} value - The current value of the textarea
 * @returns {React.RefObject<HTMLTextAreaElement>} Ref to be attached to the textarea element
 */
function useAutosizeTextarea(value) {
  /** @type {React.RefObject<HTMLTextAreaElement>} */
  const textareaRef = useRef(null);

  useLayoutEffect(() => {
    const textarea = textareaRef.current;
    if (!textarea) return;
    // Reset height to allow shrinking if content is deleted
    textarea.style.height = "auto";
    // Set height to fit the scrollHeight (actual content height)
    textarea.style.height = `${textarea.scrollHeight}px`;
    // Allow scroll if content exceeds visible area
    if (textarea.scrollHeight > textarea.clientHeight) {
      textarea.style.overflowY = "auto";
    } else {
      textarea.style.overflowY = "hidden";
    }
  }, [value]); // Re-run effect whenever the value changes

  return textareaRef;
}

export default useAutosizeTextarea;
