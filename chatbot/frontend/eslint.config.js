// eslint.config.js - ESLint configuration for React project
// Ensures code quality, best practices, and consistent style

import js from "@eslint/js"; // ESLint base JavaScript rules
import globals from "globals"; // Common global variables (browser, node, etc.)
import react from "eslint-plugin-react"; // React-specific linting rules
import reactHooks from "eslint-plugin-react-hooks"; // React Hooks linting rules
import reactRefresh from "eslint-plugin-react-refresh"; // React Fast Refresh linting

export default [
  {
    // Lint all JS and JSX files in the project
    files: ["**/*.{js,jsx}"],
    // Ignore build output and dependencies
    ignores: ["dist", "node_modules"],
    languageOptions: {
      // ECMAScript version and features
      ecmaVersion: 2020,
      globals: globals.browser, // Browser environment
      parserOptions: {
        ecmaVersion: "latest",
        ecmaFeatures: { jsx: true }, // Enable JSX
        sourceType: "module", // Use ES Modules
      },
    },
    // React version for linting
    settings: { react: { version: "18.3" } },
    // Plugins for React, Hooks, and Fast Refresh
    plugins: {
      react,
      "react-hooks": reactHooks,
      "react-refresh": reactRefresh,
    },
    // Linting rules: recommended + custom
    rules: {
      ...js.configs.recommended.rules,
      ...react.configs.recommended.rules,
      ...react.configs["jsx-runtime"].rules,
      ...reactHooks.configs.recommended.rules,
      // Allow target="_blank" without rel="noopener noreferrer"
      "react/jsx-no-target-blank": "off",
      // Warn if components are not exported as constants (for Fast Refresh)
      "react-refresh/only-export-components": [
        "warn",
        { allowConstantExport: true },
      ],
    },
  },
];
