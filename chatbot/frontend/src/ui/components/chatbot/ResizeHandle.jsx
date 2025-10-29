// ResizeHandle.jsx
// Visual handle for resizing a panel from the top-left corner.
// Triggers the resize logic when the user clicks and drags this area.

/**
 * @param {{ onMouseDown: (event: React.MouseEvent<HTMLDivElement, MouseEvent>) => void }} props
 */
export default function ResizeHandle({ onMouseDown }) {
  return (
    <div
      onMouseDown={onMouseDown}
      className="absolute top-0 left-0 w-6 h-6 z-10 cursor-nwse-resize"
    >
      <svg className="w-4 h-4 mt-1 ml-1 text-light-blue/50" viewBox="0 0 16 16">
        <line
          x1="2"
          y1="14"
          x2="14"
          y2="2"
          stroke="currentColor"
          strokeWidth="1.5"
        />
        <line
          x1="6"
          y1="14"
          x2="14"
          y2="6"
          stroke="currentColor"
          strokeWidth="1.2"
        />
      </svg>
    </div>
  );
}
