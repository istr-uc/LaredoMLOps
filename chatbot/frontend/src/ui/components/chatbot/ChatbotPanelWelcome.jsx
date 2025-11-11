/**
 * ChatbotPanelWelcome
 * Displays a sleek, product-style welcome message for the LaredocMind assistant.
 *
 * Designed to evoke the tone of futuristic tech ads, while explaining core functionality.
 */
function ChatbotPanelWelcome() {
  return (
    <div className="flex-1 overflow-auto text-light-blue text-xl font-light space-y-2 text-left">
      <br></br>
      <p aria-label="Hello" role="img">
        Welcome to the next generation of assistance.
      </p>
      <br></br>
      <p>
        Meet <strong>LaredocMind</strong>.{" "}
      </p>
      <p>
        A new way to connect with your information. Designed to understand and
        remember what matters to you.
      </p>
      <br></br>
      <p>
        It reads the documents, explores the data and understands the system so
        you don't have to.
      </p>
      <br></br>
      <p>Ask anything, from how to build a workflow to what a button does.</p>
      <p>Forget the manuals. Forget the guessing. Just ask. </p>
    </div>
  );
}

export default ChatbotPanelWelcome;
