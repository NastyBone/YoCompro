/** @type {import('tailwindcss').Config} */
const colors = require("tailwindcss/colors")
module.exports = {
  content: ["./templates/**/*.{html,js}", "./templates/*.{html,js}"],
  theme: {
    extend: {},
    colors: {
      ...colors,
      baseblue: "#0d6efd",
    },
  },
  plugins: [],
  prefix: "tw-",
}
