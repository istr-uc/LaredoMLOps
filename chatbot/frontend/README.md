# LaredocMind Frontend

## Overview

This repository is the main development workspace for the LaredocMind embeddable chatbot widget. Here, the widget is improved, tested, and built for distribution as an npm package.

**If you want to use the chatbot in your own React project, simply install the npm package and import the widget.**

---

## Installation in Your Project

Install the npm package:

```sh
npm install laredocmind
```

Then, in your React app:

```jsx
import { ChatbotWidget } from "laredocmind";

function App() {
  return (
    <ChatbotWidget apiUrl="http://localhost:20000" />
  );
}
```

---

## About this Repository

This repository contains the source code, development environment, and example/demo for the LaredocMind chatbot widget. If you want to contribute, test, or improve the widget, you can run it locally as described below.

## Description

LaredocMind Frontend is a modern, embeddable chat interface built with React and Tailwind CSS. It connects to the LaredocMind backend, allowing users to interact with an AI assistant that understands, remembers, and reasons over your documents. Designed for clarity and speed, the frontend provides a floating chat widget that can be integrated into any web application.

## Installation and Quick Start

You can set up and run the frontend using either the quick script option, the production build option, or by following the manual steps.

### Option 1: Development Server (Recommended for Development)

1. Open a terminal in the `frontend` folder.
2. Run the following command to install all dependencies:
   ```sh
   npm install
   ```
3. To start the frontend development server, run:
   ```sh
   npm run dev
   ```
4. Open your browser and go to [http://localhost:21000](http://localhost:21000) (default port).

### Option 2: Production Build (Serve from dist/)

1. Run the setup script to install dependencies and build the production frontend:
   ```sh
   setup_frontend.bat
   ```
2. To serve the production build, run:
   ```sh
   run_frontend.bat
   ```
3. Open your browser and go to [http://localhost:21000](http://localhost:21000) (the production build will be served on this port).

## Publishing the NPM Package

To publish a new version of the LaredocMind frontend package to npm, follow these steps:

1. **Build the package:**
   ```sh
   npm run build
   ```
   This will generate the production build in the `dist/` folder.

2. **Update the CSS:**
   - Copy the generated CSS file from `dist/laredocmind.css` and replace the existing CSS file in `src/ui/styles/` with the new one.
   - Make sure the new CSS is correctly referenced in your components or entry point.

3. **Update the package version:**
   - Open `package.json` and increment the `version` field according to [semantic versioning](https://semver.org/).

4. **Publish to npm:**
   ```sh
   npm publish
   ```
   Make sure you are logged in to the correct npm account (`npm login`) and have the necessary permissions to publish the package.

5. **Verify the publication:**
   - Check the npm registry or your npm account to ensure the new version is available.

## Project Structure

```
frontend/
├── src/
│   ├── app/                # Main App component
│   ├── assets/             # Static assets (icons, images)
│   ├── core/               # Core logic (API, chatbot state, hooks)
│   │   ├── api/            # API communication and error handling
│   │   ├── chatbot/        # Chatbot state, animation, storage, message utils
│   │   └── hooks/          # Custom React hooks (autosize, focus, scroll, resize, click-outside)
│   ├── pages/              # Example and future pages
│   ├── types/              # Type definitions
│   ├── ui/                 # UI components and styles
│   │   ├── components/     # Chatbot widget, message bubbles, spinner, etc.
│   │   └── styles/         # Global and component CSS (Tailwind)
│   └── main.jsx            # React entry point
├── theme/                  # Tailwind theme extensions (colors, animations, keyframes, shadows)
├── index.html              # Main HTML file
├── tailwind.config.js      # Tailwind CSS config
├── vite.config.js          # Vite config
├── package.json            # Project metadata and scripts
├── jsconfig.json           # VSCode/JS path aliases
├── .env.example            # Example environment variables
├── postcss.config.js       # PostCSS config
├── eslint.config.js        # ESLint config
└── ...                     # Other config files
```

## Detailed Folder and File Descriptions

### `src/`

Main source code, organized by responsibility:

#### `app/`

- `App.jsx`: Root React component that renders the main page and the floating LaredocMind widget.

#### `assets/`

- `images/`: SVG icons and images used throughout the UI (chat, close, error, pin, send, trash).

#### `core/`

- `api/`: Handles communication with the backend API, error handling, and endpoint management.
  - `endpoints.js`: API endpoint construction and environment variable management.
  - `errors.js`: Utility functions for API error handling.
  - `index.js`: Main API functions for sending and streaming chat messages.
- `chatbot/`: Chatbot state management, animation, storage, and message utilities.
  - `useChatbotAnimation.js`: Manages open/close state and UI animation for the chat widget.
  - `useChatbotConversation.js`: Central hook for chat state, message sending, and persistence.
  - `useChatbotMessage.js`: Utilities for creating user/assistant message objects.
  - `useChatbotStorage.js`: Handles localStorage for chat message history.
- `hooks/`: Custom React hooks for UI and UX enhancements.
  - `useAutosizeTextarea.js`: Autosizes chat input textarea.
  - `useClickOutside.js`: Detects clicks outside a referenced element.
  - `useFocusOnOpen.js`: Focuses input when the chat opens.
  - `useResizablePanel.js`: Makes the chat panel resizable from the corner.
  - `useScrollToBottom.js`: Auto-scrolls the chat to the latest message.

#### `pages/`

- `ExamplePage.jsx`: Example page to demonstrate the floating chat widget.

#### `types/`

- `vite-env.d.ts`: TypeScript type definitions for Vite environment variables.

#### `ui/`

- `components/`: Modular UI components for the chat widget.
  - `ChatbotWidget.jsx`: Encapsulates the chat widget for easy embedding.
  - `chatbot/`: Floating panel, button, controls, input area, messages area, welcome message, portal logic, and resize handle.
  - `message/`: Message bubble, error, input, list, loading indicator, send button, and textarea components.
  - `spinner/`: Spinner and spinner container for loading states.
- `styles/`: Global and component CSS (Tailwind), including scrollbar and markdown styling.

### `theme/`

- `animations.js`: Custom animation definitions for Tailwind.
- `colors.js`: Custom color palette for Tailwind.
- `keyframes.js`: Keyframes for chat UI animations.
- `shadows.js`: Centralized box-shadow definitions.

### Root Configuration Files

- `index.html`: Main HTML file for the frontend app.
- `tailwind.config.js`: Tailwind CSS configuration.
- `vite.config.js`: Vite build and dev server configuration.
- `package.json`: Project metadata, scripts, and dependencies.
- `jsconfig.json`: VSCode/JS path aliases and project settings.
- `.env.example`: Example environment variables for configuration.
- `postcss.config.js`: PostCSS configuration for CSS processing.
- `eslint.config.js`: ESLint configuration for code quality.

## Troubleshooting

### Common Issues

- **API Not Responding**: Make sure the backend is running.
- **Port Conflicts**: If the frontend fails to start, verify that port 21000 is not in use by another process.
- **Dependency Problems**: Ensure all dependencies are installed with `npm install` and that you are using a compatible Node.js version.
- **Build Errors**: If you encounter build errors, try deleting `node_modules` and running `npm install` again.

### Verifying the Frontend

- To verify the frontend is running correctly, open your browser and go to `http://localhost:21000`. You should see the LaredocMind chat widget floating in the bottom-right corner.

### Debugging

- Use your browser's developer tools (F12) to inspect errors, network requests, and console logs.
- Check the terminal output for errors when running `npm run dev` or `npm run build`.

## License

This project is licensed under the MIT License. You are free to use, modify, and distribute this software, provided that the original copyright and license notice are included.

See the `LICENSE` file for the full license text.
