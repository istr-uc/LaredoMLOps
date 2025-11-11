// useFocusOnOpen.js - Custom React hook for focusing input on open
// ---------------------------------------------------------------
// This hook automatically focuses a referenced input or textarea when a component becomes visible.

import { useEffect } from "react";

/**
 * useFocusOnOpen - Custom React hook
 *
 * Automatically focuses the provided inputRef when isVisible becomes true.
 *
 * @param {boolean} isVisible - Whether the input should be focused (e.g., when a modal or chat opens)
 * @param {React.RefObject<HTMLElement>} inputRef - Ref to the input or textarea element to focus
 */
function useFocusOnOpen(isVisible, inputRef) {
  useEffect(() => {
    // Focus only if the component is visible, the ref is attached, and the element is not already focused
    if (
      isVisible &&
      inputRef.current &&
      document.activeElement !== inputRef.current
    ) {
      inputRef.current.focus();
    }
  }, [isVisible, inputRef]); // Re-run when visibility or ref changes
}

export default useFocusOnOpen;
