// useScrollToBottom.js - Optimized React hook for auto-scrolling containers
// ---------------------------------------------------------------------
// This hook ensures a scrollable container always scrolls to the bottom when dependencies change.
// Useful for chat UIs and live logs.

import { useRef, useEffect } from "react";

/**
 * useScrollToBottom
 *
 * Custom React hook that scrolls a container to the bottom or top (user message) whenever dependencies change.
 *
 * @param {Array<any>} dependencies - Dependency array to trigger auto-scroll (e.g., [messages.length, isLoading, lastMessageRole, lastMessageContent]).
 *   - It's important to include lastMessage?.content as a dependency for streaming updates.
 * @param {string} [lastMessageRole] - Role of the last message ("user" or "assistant"). Used to determine scroll direction.
 *   - If 'user' and not loading, scrolls to top (shows user's message at the top).
 *   - If 'assistant' or loading, scrolls to bottom (shows assistant's message or streaming at the bottom).
 * @returns {React.RefObject<HTMLDivElement>} Ref to attach to the scrollable container.
 */
function useScrollToBottom(dependencies = [], lastMessageRole) {
  /** @type {React.RefObject<HTMLDivElement>} */
  const containerRef = useRef(null);
  const isFirstScroll = useRef(true);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;
    const extraOffset = 40; // Small offset for visual comfort at the bottom
    // --- SCROLL LOGIC ---
    // If the last message is from the user and not loading, scroll to the top (show user's message at the top)
    // Otherwise (assistant or streaming), scroll to the bottom (show latest assistant message or streaming progress)
    if (lastMessageRole === "user" && !dependencies.includes(true)) {
      container.scrollTo({
        top: 0,
        behavior: isFirstScroll.current ? "auto" : "smooth",
      });
    } else {
      container.scrollTo({
        top: container.scrollHeight + extraOffset,
        behavior: isFirstScroll.current ? "auto" : "smooth",
      });
    }
    isFirstScroll.current = false;
  }, [...dependencies, lastMessageRole]);

  return containerRef;
}

export default useScrollToBottom;
