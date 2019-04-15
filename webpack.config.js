const path = require('path')
const src_dir = './static/js/'
const build_dir = './static/js/'

module.exports = {
  mode: 'development',
  entry: src_dir + 'index.js',
  resolve: {
    extensions: [ '.js' ]
  },
  output: {
    filename: 'scripts.js',
    path: path.join(__dirname, build_dir)
  },
  devtool: 'sourcemap'
}