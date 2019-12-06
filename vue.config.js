let path = require('path');
const BundleTracker = require("webpack-bundle-tracker");
const devMode = process.env.NODE_ENV !== 'production';

module.exports = {
  publicPath: devMode ? 'http://localhost:8080' : './',
  outputDir: 'dist',
  runtimeCompiler: true,
  assetsDir: 'static',
  configureWebpack: {
    devtool: 'source-map',
    resolve: {
      alias: {
        '@': path.join(__dirname, './static/src')
      }
    },
    devServer: {
      historyApiFallback: true,
      // noInfo: true,
    },
    entry: {
      app: path.join(__dirname, './static/src', 'main.js')
    }
  },
  css: {
    loaderOptions: {
      css: {
        // options here will be passed to css-loader
      },
      sass: {
        indentWidth: 4,
        includePaths: ['src/assets/css/style.scss'],
      }
    }
  },
  chainWebpack: config => {
    config.optimization
        .splitChunks(false);

    config
        .plugin('BundleTracker')
        .use(BundleTracker, [{filename: './webpack-stats.json'}]);

    config.resolve.alias
        .set('__STATIC__', 'static');

    config.devServer
        .public('http://0.0.0.0:8080')
        .host('0.0.0.0')
        .port(8080)
        .hotOnly(true)
        .watchOptions({poll: 1000})
        .https(false)
        .headers({"Access-Control-Allow-Origin": ["\*"]})
  }
};

