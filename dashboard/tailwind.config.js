/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "#f8fafc",
        card: "#ffffff",
        primary: "#16a34a", // Green-600
        secondary: "#22c55e", // Green-500
        accent: "#15803d", // Green-700
        textMain: "#1e293b", // Slate-800
        textMuted: "#64748b", // Slate-500
      },
      animation: {
        'pulse-slow': 'pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      }
    },
  },
  plugins: [],
}
