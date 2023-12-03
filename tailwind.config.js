/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./**/*.html",
  "node_modules/preline/dist/*.js",
  ],
  theme: {
    extend: {
      fontFamily: {
        'sans': ['Satoshi', 'system-ui'],
      }
    },
  },
  plugins: [
    require('preline/plugin'),
  ],
  darkMode: 'class',
}

