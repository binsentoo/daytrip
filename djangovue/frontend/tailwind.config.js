/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["dist/**/*.{html,js,vue}", 
            "dist/*.{html,js,vue}", 
            "src/*.{html,js,vue}",
            "src/**/*.{html,js,vue}",
  ],
  theme: {
    extend: {
      fontFamily: {
        poppins: ['Poppins', 'sans-serif'],
      }
    },
  },
  plugins: [],
}

