/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./**/*.html",
  "node_modules/preline/dist/*.js",
  ],
  theme: {
    extend: {
      fontFamily: {
        'sans': ['Satoshi-Regular', 'system-ui'],
      }
    },
  },
  plugins: [
    require('preline/plugin'),
  ],
}

