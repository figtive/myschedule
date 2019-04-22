const path = require('path');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

module.exports = {
  entry: { main: './static/index.js' },
  output: {
    path: path.join(__dirname, 'static'),
    filename: 'script.js'
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        include: [
          path.join(__dirname, "static/css"), 
          path.join(__dirname, "node_modules")
        ],
        use: {
          loader: "babel-loader"
        }
      },
      {
        test: /(\.scss$)|(\.css$)/,
        include: [
          path.join(__dirname, "static/css"), 
          path.join(__dirname, "node_modules")
        ],
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