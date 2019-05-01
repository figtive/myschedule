const path = require('path');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

module.exports = {
  entry: { main: './static/index.js' },
  output: {
    path: path.join(__dirname, 'static/dist'),
    filename: 'script.js'
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        use: {
          loader: "babel-loader"
        }
      },
      {
        test: /(\.scss$)|(\.css$)/,
        use: [
          "style-loader",
          MiniCssExtractPlugin.loader,
          "css-loader",
          "sass-loader"
        ]
      }
    ]
  }, 
  plugins: [
    new MiniCssExtractPlugin({
      filename: 'style.css',
    })
  ]
};