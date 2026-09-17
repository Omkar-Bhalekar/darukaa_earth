/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        forest: {
          green: '#1B4332',
        },
        sage: {
          DEFAULT: '#52796F',
          light: '#B7E4C7',
        },
        sand: {
          warm: '#D4A373',
        },
        earth: {
          brown: '#6B4226',
        },
        sky: {
          blue: '#89C2D9',
        },
        off: {
          white: '#FEFAE0',
        },
        charcoal: {
          DEFAULT: '#2D3436',
        }
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        heading: ['Space Grotesk', 'sans-serif'],
      },
      spacing: {
        '8px': '8px',
      },
      borderRadius: {
        'xl': '12px',
        'lg': '8px',
      },
      transitionDuration: {
        DEFAULT: '200ms',
      }
    },
  },
  plugins: [],
}
