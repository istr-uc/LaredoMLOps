// Main entry point for the React application
import React from "react";
import { createRoot } from "react-dom/client";
import App from "./app/App.jsx";
import "@/ui/styles/index.css"

// Select the root element from the HTML where the React app will be mounted
const rootElement = document.getElementById("root");

if (rootElement) {
  // Create a React root and render the App component inside React.StrictMode
  createRoot(rootElement).render(
    <React.StrictMode>
      <App />
    </React.StrictMode>,
  );
}
