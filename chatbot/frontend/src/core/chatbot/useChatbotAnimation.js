import { useState, useEffect, useCallback } from "react";

// Animation durations (ms)
const BUTTON_ANIMATION_DURATION = 300; // Button expand/contract
const PANEL_ANIMATION_DURATION = 200; // Panel expand/contract

// Animation class names (Tailwind CSS)
const ANIMATION_BUTTON_EXPAND = "animate-chatbot-button-expand";
const ANIMATION_BUTTON_CONTRACT = "animate-chatbot-button-contract";
const ANIMATION_PANEL_ENTER = "animate-chatbot-panel-expand";
const ANIMATION_PANEL_EXIT = "animate-chatbot-panel-contract";

/**
 * useChatbotAnimation
 *
 * Custom React hook to manage all animation state and transitions for the chatbot button and panel.
 *
 * Features:
 * - Controls open/close state of the chatbot panel
 * - Manages animation classes for entrance/exit transitions (panel & button)
 * - Handles visibility and animation of the floating chatbot button
 * - Exposes booleans and handlers for UI logic (e.g., isPanelAnimatingOut)
 *
 * Usage:
 *   const {
 *     isOpen,                // true if panel is open
 *     showButton,            // true if floating button should be visible
 *     buttonAnimation,       // animation class for the button
 *     panelAnimation,        // animation class for the panel
 *     isPanelAnimatingOut,   // true if panel is animating out (closing)
 *     handlePanelOpen,       // call to open panel (with animation)
 *     handlePanelClose,      // call to close panel (with animation)
 *     setIsOpen,             // advanced: manually set open state
 *   } = useChatbotAnimation();
 *
 * All animation timing and class names are encapsulated here for maintainability.
 */
function useChatbotAnimation() {
  // State: whether the chatbot panel is open (mounted)
  const [isOpen, setIsOpen] = useState(false);
  // State: whether the floating chatbot button is visible
  const [showButton, setShowButton] = useState(true);
  // State: animation class for the chatbot button (expand/contract)
  const [buttonAnimation, setButtonAnimation] = useState("");
  // State: animation class for the chatbot panel (enter/exit)
  const [panelAnimation, setPanelAnimation] = useState("");

  // Derived: true if the panel is currently animating out (exit transition)
  const isPanelAnimatingOut = panelAnimation === ANIMATION_PANEL_EXIT;

  /**
   * Opens the chatbot panel with entrance animation.
   * - Expands the button
   * - Shows the panel with enter animation
   * - Hides the button after expand animation completes
   */
  const handlePanelOpen = useCallback(() => {
    setButtonAnimation(ANIMATION_BUTTON_EXPAND);
    setShowButton(true);
    setTimeout(() => {
      setPanelAnimation(ANIMATION_PANEL_ENTER);
      setIsOpen(true);
      setTimeout(() => setShowButton(false), BUTTON_ANIMATION_DURATION);
    }, 0); // Defer to next tick for smooth transition
  }, []);

  /**
   * Closes the chatbot panel with exit animation.
   * - Triggers panel exit animation
   * - Shows and contracts the button after panel closes
   * - Resets button animation after contract
   */
  const handlePanelClose = useCallback(() => {
    if (!isOpen) return;
    setPanelAnimation(ANIMATION_PANEL_EXIT);
    setTimeout(() => {
      setShowButton(true);
      setButtonAnimation(ANIMATION_BUTTON_CONTRACT);
      setTimeout(() => setButtonAnimation(""), BUTTON_ANIMATION_DURATION);
    }, PANEL_ANIMATION_DURATION); // Wait for panel exit animation
  }, [isOpen]);

  /**
   * Unmounts the panel after exit animation completes.
   * - When animating out, waits for exit duration then unmounts panel
   * - Cleans up panel animation class
   */
  useEffect(() => {
    if (panelAnimation === ANIMATION_PANEL_EXIT) {
      const timer = setTimeout(() => {
        setIsOpen(false);
        setPanelAnimation("");
      }, PANEL_ANIMATION_DURATION);
      return () => clearTimeout(timer);
    }
  }, [panelAnimation]);

  // Return all animation state and handlers for the chatbot UI
  return {
    isOpen, // true if panel is open
    showButton, // true if floating button should be visible
    buttonAnimation, // animation class for the button
    panelAnimation, // animation class for the panel
    handlePanelOpen, // call to open panel (with animation)
    handlePanelClose, // call to close panel (with animation)
    setIsOpen, // advanced: manually set open state
    isPanelAnimatingOut, // true if panel is animating out (exit)
  };
}

export default useChatbotAnimation;
