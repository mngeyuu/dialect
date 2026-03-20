module.exports = {
  publicPath: './',
  parallel: false,

  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/media': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  },

  configureWebpack: {
    performance: {
      hints: false
    }
  },

  pluginOptions: {
    electronBuilder: {
      nodeIntegration: false,
      preload: 'src/preload.js',
      builderOptions: {
        appId: 'com.yourapp.dialect',
        productName: '方言词汇查询系统',
        copyright: 'Copyright © 2025',
        win: {
          icon: 'build/icons/icon.ico'
        },
        mac: {
          icon: 'build/icons/icon.icns'
        },
        extraResources: [
          {
            from: 'public/audio',
            to: 'audio'
          }
        ],
        directories: {
          output: 'dist_electron'
        }
      }
    }
  }
}
