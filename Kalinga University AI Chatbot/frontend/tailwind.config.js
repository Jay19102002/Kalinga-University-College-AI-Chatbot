/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        neu: {
          bg: '#e0e5ec',
          light: '#ffffff',
          dark: '#a3b1c6',
          darker: '#909fb7',
          accent: '#2563eb'
        },
        kalinga: {
          50: '#f0f4ff',
          100: '#e0eaff',
          500: '#2563eb',
          600: '#1d4ed8',
          700: '#1e40af',
          800: '#1e3a8a',
          900: '#0f172a',
          gold: '#f59e0b',
          maroon: '#800000',
          bg: '#e0e5ec'
        }
      },
      boxShadow: {
        'neu-extruded': '8px 8px 16px #a3b1c6, -8px -8px 16px #ffffff',
        'neu-extruded-lg': '14px 14px 28px #a3b1c6, -14px -14px 28px #ffffff',
        'neu-extruded-sm': '4px 4px 8px #a3b1c6, -4px -4px 8px #ffffff',
        'neu-pressed': 'inset 4px 4px 8px #a3b1c6, inset -4px -4px 8px #ffffff',
        'neu-pressed-deep': 'inset 6px 6px 12px #909fb7, inset -6px -6px 12px #ffffff',
        'neu-button': '6px 6px 12px #a3b1c6, -6px -6px 12px #ffffff',
        'neu-button-active': 'inset 3px 3px 6px #a3b1c6, inset -3px -3px 6px #ffffff',
        'neu-blue-glow': '6px 6px 14px #9bb2d4, -6px -6px 14px #ffffff, 0 0 15px rgba(37, 99, 235, 0.3)',
        'neu-badge': 'inset 2px 2px 4px #a3b1c6, inset -2px -2px 4px #ffffff'
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif']
      }
    },
  },
  plugins: [],
}
