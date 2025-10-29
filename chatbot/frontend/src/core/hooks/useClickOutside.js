// useClickOutside.js - Custom React hook for detecting outside clicks
// ---------------------------------------------------------------
// This hook calls a handler function when a click occurs outside a referenced element.

import { useEffect, useCallback } from "react";

/**
 * useClickOutside - Custom React hook
 *
 * Calls the handler when a click outside the referenced element occurs, if enabled.
 *
 * @param {React.RefObject<HTMLElement>} ref - Ref to the element to detect outside clicks for
 * @param {() => void} handler - Function to call when an outside click is detected
 * @param {boolean} enabled - Whether the outside click detection is active
 */
function useClickOutside(ref, handler, enabled) {
  // Memoize the event handler to avoid unnecessary re-renders
  const memoizedHandler = useCallback(
    (event) => {
      // Get the event path (supports Shadow DOM)
      const path = event.composedPath ? event.composedPath() : [];
      // If any node in the path has the .chatbot-widget class, do not trigger handler
      if (
        path.some(
          (node) => node.classList && node.classList.contains("chatbot-widget")
        )
      )
        return;
      // If the ref still exists and contains the event target, do not trigger handler
      if (ref.current && ref.current.contains(event.target)) return;
      // Otherwise, call the handler (outside click detected)
      handler();
    },
    [ref, handler]
  );

  useEffect(() => {
    // Only add the event listener if enabled
    if (!enabled) return;
    // Listen for mousedown events in the capture phase
    window.addEventListener("mousedown", memoizedHandler, true); // capture phase
    return () => {
      // Clean up the event listener on unmount or when disabled
      window.removeEventListener("mousedown", memoizedHandler, true);
    };
  }, [enabled, memoizedHandler]);
}

export default useClickOutside;
