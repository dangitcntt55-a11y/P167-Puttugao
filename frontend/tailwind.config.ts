import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        brand: {
          primary: "#3b82f6", // blue (target brand)
          competitor: "#94a3b8", // gray
          improved: "#10b981", // green
          no_evidence: "#f59e0b", // yellow
          regressed: "#ef4444", // red
        },
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
};

export default config;
