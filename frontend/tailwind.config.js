export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        ois: {
          dark:    "#0F172A",
          surface: "#1E293B",
          border:  "#334155",
          accent:  "#3B82F6",
          success: "#10B981",
          warning: "#F59E0B",
          danger:  "#EF4444",
          text:    "#F1F5F9",
          muted:   "#94A3B8",
        }
      }
    }
  },
  plugins: [],
}