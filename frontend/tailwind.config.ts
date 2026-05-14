import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./features/**/*.{ts,tsx}",
    "./services/**/*.{ts,tsx}",
    "./hooks/**/*.{ts,tsx}"
  ],
  theme: {
    extend: {
      colors: {
        ink: "#0F172A",
        slatepanel: "#111827",
        border: "#E5E7EB",
        accent: "#0F766E"
      },
      boxShadow: {
        card: "0 18px 40px rgba(15, 23, 42, 0.08)"
      },
      backgroundImage: {
        "hero-grid":
          "radial-gradient(circle at top, rgba(15,118,110,0.18), transparent 35%), linear-gradient(135deg, rgba(255,255,255,0.95), rgba(238,242,255,0.92))"
      }
    }
  },
  plugins: []
};

export default config;
