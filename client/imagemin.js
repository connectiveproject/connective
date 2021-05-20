const imagemin = require("imagemin")
const imageminWebp = require("imagemin-webp")
const imagesFolder = "src/assets/img/"

imagemin([`${imagesFolder}/original/small/*`], {
  destination: `${imagesFolder}/optimized`,
  plugins: [imageminWebp({ quality: 100 })],
}).then(() => {
  console.log("+ Small Images Optimization: Success!")
})

imagemin([`${imagesFolder}/original/big/*`], {
  destination: `${imagesFolder}/optimized`,
  plugins: [imageminWebp({ quality: 50 })],
}).then(() => {
  console.log("+ Big Images Optimization: Success!")
})
