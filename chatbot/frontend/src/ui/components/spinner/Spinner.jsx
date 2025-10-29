/**
 * Spinner Component
 *
 * Displays a dual-layer animated spinner.
 * Used to indicate loading states in the UI.
 * The animation is controlled via CSS classes: `animate-chatbot-spinner` and `animate-chatbot-spinner-delayed`.
 */
function Spinner() {
  return (
    <div className="relative h-9 w-6 flex items-center justify-center">
      {/* First spinner layer (starts immediately) */}
      <span className="spinner-child animate-chatbot-spinner shadow-spinner" />

      {/* Second spinner layer (starts with a slight delay) for a layered effect */}
      <span className="spinner-child animate-chatbot-spinner-delayed shadow-spinner" />
    </div>
  );
}

export default Spinner;
