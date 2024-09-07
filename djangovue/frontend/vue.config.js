const { defineConfig } = require('@vue/cli-service')
const pages = {  
  index: "src/js/main.js",
  login: "src/js/login.js"
};  
  
module.exports = {  
  transpileDependencies: true,
  publicPath: "/dist",
  outputDir: "dist",
  indexPath: "index.html",
  
  pages: pages,  
  
};