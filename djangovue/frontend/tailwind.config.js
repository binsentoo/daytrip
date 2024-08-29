/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["build/templates/**/*.{html,js,vue}", 
            "build/templates/*.{html,js,vue}", 
            "src/*.{html,js,vue}",
            "src/components/*.{html,js,vue}"
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

