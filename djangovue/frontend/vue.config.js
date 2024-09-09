const { defineConfig } = require('@vue/cli-service')

module.exports = {  
  transpileDependencies: true,
  publicPath: process.env.NODE_ENV === 'production'
    ? '/'
    : '/',
  outputDir: "dist",
  indexPath: "index.html",
  
  pages: {
    index: {
      // entry for the page
      entry: 'src/js/main.js',
      // the source template
      template: 'public/index.html',
      // output as dist/index.html
      filename: 'index.html',
    },
    // when using the entry-only string format,
    // template is inferred to be `public/subpage.html`
    // and falls back to `public/index.html` if not found.
    // Output filename is inferred to be `subpage.html`.
    login: 'src/js/login.js'
  }
};