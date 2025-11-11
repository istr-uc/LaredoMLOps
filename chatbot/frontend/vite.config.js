import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";
import tailwindcss from "@tailwindcss/vite";
import { peerDependencies } from "./package.json";
export default defineConfig({
  // Dev server configuration
  server: {
    port: 21000,
    host: true,
  },
  resolve: {
    alias: {
      "@/": path.resolve(__dirname, "./src") + "/",
    },
  },

  build: {
    lib: {
      entry: "src/index.js",
      name: "laredocmind",
      fileName: (format) => `laredocmind.${format}.js`,
      formats: ["es", "cjs", "umd"],
    },
    rollupOptions: {
      external: Object.keys(peerDependencies),
      output: {
        globals: {
          react: "React",
          "react-dom": "ReactDOM",
          "react-markdown": "ReactMarkdown",
          "react-shadow": "ReactShadow",
        },
      },
    },
  },
  // Plugins array (add more plugins as needed)
  plugins: [
    react(),
    tailwindcss(),
    // Add more plugins here
  ],
});
