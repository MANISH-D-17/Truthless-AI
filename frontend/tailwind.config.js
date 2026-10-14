/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#f0f7ff',
          100: '#e0effe',
          500: '#0284c7',
          600: '#0369a1',
          700: '#075985',
          900: '#0c4a6e',
        },
        medical: {
          dark: '#0b132b',
          navy: '#1c2541',
          teal: '#3a506b',
          cyan: '#5bc0be',
          accent: '#6fffe9',
        }
      },
    },
  },
  plugins: [],
}
