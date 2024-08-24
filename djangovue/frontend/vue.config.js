const { defineConfig } = require('@vue/cli-service')
const pages = {  
  index: "src/main.js",  
};  
  
module.exports = {  
  transpileDependencies: true,
  publicPath: "/static/vue/",
  outputDir: "./build/static/vue/",
  indexPath: "../../templates/vue_index.html",
  
  pages: pages,  
  
};