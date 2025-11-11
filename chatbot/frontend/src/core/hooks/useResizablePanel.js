// useResizablePanel.js has been moved to the shared hooks folder for better code organization.
// Please update your imports to:
// import { useResizablePanel } from "@/core/hooks/useResizablePanel";

// useResizablePanel.js
// -----------------------------------------------------------------------------
// Custom React hook for making a panel resizable from the top-left corner.
// Handles mouse events, state, and provides style and event handler for the panel.

import { useState, useRef } from "react";

/**
 * useResizablePanel
 *
 * Provides resize logic, style, and event handler for a resizable panel UI.
 *
 * @param {Object} options
 * @param {React.RefObject<HTMLElement>} options.containerRef - Ref for the panel container (optional, for future use)
 * @returns {{
 *   size: {width: number, height: number},
 *   resizing: boolean,
 *   panelStyle: React.CSSProperties,
 *   handleResizeHandleMouseDown: (event: React.MouseEvent) => void
 * }}
 *
 */
export function useResizablePanel({ containerRef }) {
  // Calculate initial size based on viewport, with min/max constraints
  const getInitialSize = () => ({
    width: Math.min(
      Math.max(480, window.innerWidth * 0.5),
      window.innerWidth * 0.9,
    ),
    height: Math.min(
      Math.max(400, window.innerHeight * 0.9),
      window.innerHeight * 0.9,
    ),
  });

  // State for panel size and whether resizing is active
  const [size, setSize] = useState(getInitialSize);
  const [resizing, setResizing] = useState(false);

  // Internal refs for drag logic
  const resizingRef = useRef(false);
  const startPos = useRef({ x: 0, y: 0 });
  const startSize = useRef(getInitialSize());

  // Start resizing on mousedown (native event)
  /** @param {MouseEvent} e */
  const handleMouseDown = (e) => {
    setResizing(true);
    resizingRef.current = true;
    startPos.current = { x: e.clientX, y: e.clientY };
    startSize.current = { ...size };
    document.addEventListener("mousemove", handleMouseMove);
    document.addEventListener("mouseup", handleMouseUp);
  };

  // Update panel size on mousemove (native event)
  /** @param {MouseEvent} e */
  const handleMouseMove = (e) => {
    if (!resizingRef.current) return;
    const dx = startPos.current.x - e.clientX;
    const dy = startPos.current.y - e.clientY;
    setSize({
      width: Math.max(
        320,
        Math.min(startSize.current.width + dx, window.innerWidth * 0.9),
      ),
      height: Math.max(
        400,
        Math.min(startSize.current.height + dy, window.innerHeight * 0.9),
      ),
    });
  };

  // Stop resizing on mouseup (native event)
  const handleMouseUp = () => {
    resizingRef.current = false;
    setResizing(false);
    document.removeEventListener("mousemove", handleMouseMove);
    document.removeEventListener("mouseup", handleMouseUp);
  };

  // React event handler for the resize handle
  /** @param {React.MouseEvent} event */
  const handleResizeHandleMouseDown = (event) => {
    event.preventDefault();
    handleMouseDown(event.nativeEvent);
  };

  // Panel style object, including pointer-events for resize lock
  const panelStyle = {
    width: size.width,
    height: size.height,
    minWidth: 320,
    minHeight: 400,
    maxWidth: "90vw",
    maxHeight: "90vh",
    pointerEvents: resizing ? "none" : "auto",
    position: "relative",
  };

  return {
    size,
    resizing,
    // @ts-ignore
    panelStyle,
    handleResizeHandleMouseDown,
  };
}
