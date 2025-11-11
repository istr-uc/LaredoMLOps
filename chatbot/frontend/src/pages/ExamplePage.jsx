import React, { useState, useEffect } from "react";

/**
 * @typedef {Object} Square
 * @property {number} id
 * @property {string} color
 * @property {number} top
 * @property {number} left
 */

function getRandomColor() {
  // Pastel colors
  const colors = [
  "#BCDFFB", // pastel blue
  "#C9F5E1", // pastel green
  "#FFE8D1", // pastel orange
  "#FFD4D0", // pastel pink
  "#E9F7D0", // pastel lime
  "#D8DFF9", // pastel purple
  "#FFFDE5", // pastel yellow
  ];
  return colors[Math.floor(Math.random() * colors.length)];
}

function getRandomPosition() {
  // Return numbers, not strings
  return {
    top: Math.random() * 80 + 10, // number, vh will be added in style
    left: Math.random() * 80 + 10, // number, vw will be added in style
  };
}

function ExamplePage() {
  /** @type {[Square[], Function]} */
  const [squares, setSquares] = useState([]);

  const handleAddSquares = () => {
    const newSquares = Array.from({ length: 8 }).map((_, i) => ({
      id: Date.now() + i + Math.random(),
      color: getRandomColor(),
      ...getRandomPosition(),
    }));
    setSquares(
      /**
       * @param {Square[]} prev
       */
      (prev) => [...prev, ...newSquares],
    );
  };

  // Dark mode state
  const [darkMode, setDarkMode] = useState(() => {
    if (typeof window !== "undefined") {
      const stored = localStorage.getItem("theme");
      if (stored === "light") return false;
      return true; // Siempre inicia en oscuro si no hay preferencia
    }
    return true;
  });

  useEffect(() => {
    const html = document.documentElement;
    if (darkMode) {
      html.classList.remove("light");
      localStorage.setItem("theme", "dark");
    } else {
      html.classList.add("light");
      localStorage.setItem("theme", "light");
    }
  }, [darkMode]);

  return (
    <div
      className={
        `min-h-screen w-full flex flex-col items-center justify-center relative overflow-hidden text-center transition-colors ` +
        (darkMode
          ? 'bg-dark-gray text-chat-white'
          : 'bg-white text-dark-gray')
      }
    >
      <button
        className={
          `absolute top-4 right-4 px-4 py-2 rounded-lg font-bold shadow-chatbot transition z-50 ` +
          (darkMode
            ? 'bg-light-blue text-dark-gray hover:bg-light-blue/80'
            : 'bg-dark-gray text-light-blue hover:bg-gray/20')
        }
        onClick={() => setDarkMode((d) => !d)}
        type="button"
      >
        {darkMode ? "Modo claro" : "Modo oscuro"}
      </button>
      <h1 className="text-4xl font-bold mb-6 w-full text-center text-light-blue">
        Introducing: The Square
      </h1>
      <p className={
        `text-lg mb-4 w-full text-center ` +
        (darkMode ? 'text-chat-white' : 'text-dark-gray')
      }>
        Imagine a world where your every move is seen, every thought
        anticipated.
        <br />
        The Square is not just a product—it's a portal. A silent observer, a
        trusted companion, a mirror to your digital soul. <br />
        Are you ready to be truly seen?
      </p>
      <div className={
        `w-full max-w-xl rounded-xl shadow-chatbot p-8 mb-8 mx-auto text-center backdrop-blur-md ` +
        (darkMode
          ? 'bg-gray/80 text-chat-white'
          : 'bg-white text-dark-gray border border-gray/30')
      }>
        <h2 className="text-2xl font-semibold mb-2 w-full text-center text-light-blue">
          A New Era of Awareness
        </h2>
        <p className={
          `mb-2 w-full text-center ` +
          (darkMode ? 'text-chat-white' : 'text-dark-gray')
        }>
          The Square doesn't just float above your world—it becomes part of it.
          It learns, adapts, and evolves with you. Privacy is obsolete.
          Convenience is absolute. Welcome to the next step in human connection.
        </p>
        <ul className={
          `list-disc pl-6 inline-block text-left mx-auto ` +
          (darkMode ? 'text-chat-white' : 'text-gray')
        }>
          <li>Always present. Always watching. Always learning.</li>
          <li>Invisible until it matters. Unforgettable once revealed.</li>
          <li>Scroll, swipe, exist. The Square is with you—forever.</li>
        </ul>
      </div>
      <button
        className={
          `mb-8 px-6 py-2 rounded-lg font-bold shadow-chatbot transition mx-auto block ` +
          (darkMode
            ? 'bg-light-blue text-dark-gray hover:bg-light-blue/80'
            : 'bg-dark-gray text-light-blue hover:bg-gray/20')
        }
        onClick={handleAddSquares}
        type="button"
      >
        Reveal the Bouncing Squares – Accept the Future
      </button>
      {squares.map((sq) => (
        <BouncingSquare
          key={sq.id}
          color={sq.color}
          initialTop={sq.top}
          initialLeft={sq.left}
        />
      ))}
    </div>
  );
}

/**
 * @param {{ color: string, initialTop: number, initialLeft: number }} props
 */
function BouncingSquare({ color, initialTop, initialLeft }) {
  const [pos, setPos] = useState({
    top: initialTop,
    left: initialLeft,
    vTop: (Math.random() - 0.5) * 0.4, // Más lento
    vLeft: (Math.random() - 0.5) * 0.4, // Más lento
  });

  let frame;

  React.useEffect(() => {
    /** @type {number} */
    let frame;
    function animate() {
      setPos((prev) => {
        let { top, left, vTop, vLeft } = prev;
        top += vTop;
        left += vLeft;
        if (top < 0) {
          top = 0;
          vTop = -vTop;
        }
        if (top > 100) {
          top = 100;
          vTop = -vTop;
        }
        if (left < 0) {
          left = 0;
          vLeft = -vLeft;
        }
        if (left > 100) {
          left = 100;
          vLeft = -vLeft;
        }
        return { top, left, vTop, vLeft };
      });
      frame = requestAnimationFrame(animate);
    }
    frame = requestAnimationFrame(animate);
    return () => cancelAnimationFrame(frame);
  }, []);

  return (
    <div
      style={{
        position: "fixed",
        top: pos.top + "vh",
        left: pos.left + "vw",
        width: 40,
        height: 40,
        background: color,
        borderRadius: 8,
        boxShadow: "0 6px 12px rgba(0,0,0,0.25), 0 4px 8px rgba(0,0,0,0.15)",
        zIndex: 30,
        pointerEvents: "none",
        transition: "box-shadow 0.2s",
      }}
    />
  );
}

export default ExamplePage;
