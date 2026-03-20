// background.js
'use strict'

import { app, protocol, BrowserWindow, ipcMain, dialog } from 'electron'
import { createProtocol } from 'vue-cli-plugin-electron-builder/lib'
import installExtension, { VUEJS_DEVTOOLS } from 'electron-devtools-installer'
import path from 'path'
import fs from 'fs'

const isDevelopment = process.env.NODE_ENV !== 'production'

// 保持window对象的全局引用，避免被JavaScript GC（垃圾回收）
let win

protocol.registerSchemesAsPrivileged([
  { scheme: 'app', privileges: { secure: true, standard: true } }
])

async function createWindow() {
  // 创建浏览器窗口
  win = new BrowserWindow({
    width: 1280,
    height: 800,
    webPreferences: {
      // 使用devTools插件
      nodeIntegration: process.env.ELECTRON_NODE_INTEGRATION,
      contextIsolation: !process.env.ELECTRON_NODE_INTEGRATION,
      preload: path.join(__dirname, 'preload.js')
    }
  })

  if (process.env.WEBPACK_DEV_SERVER_URL) {
    // 开发环境
    await win.loadURL(process.env.WEBPACK_DEV_SERVER_URL)
    if (!process.env.IS_TEST) win.webContents.openDevTools()
  } else {
    createProtocol('app')
    // 生产环境
    win.loadURL('app://./index.html')
  }

  win.on('closed', () => {
    win = null
  })
}

// 当Electron完成初始化并准备创建浏览器窗口时调用此方法
app.on('ready', async () => {
  if (isDevelopment && !process.env.IS_TEST) {
    // 安装Vue Devtools
    try {
      await installExtension(VUEJS_DEVTOOLS)
    } catch (e) {
      console.error('Vue Devtools failed to install:', e.toString())
    }
  }
  createWindow()
})

// 当所有窗口关闭时退出应用
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('activate', () => {
  if (win === null) {
    createWindow()
  }
})

// 这部分代码处理音频文件访问，确保应用可以访问本地文件
ipcMain.handle('get-audio-file', async (event, filePath) => {
  try {
    // 将相对路径转换为绝对路径
    const absolutePath = path.join(app.getAppPath(), 'audio', filePath)
    
    // 检查文件是否存在
    if (fs.existsSync(absolutePath)) {
      return { success: true, path: absolutePath }
    } else {
      return { success: false, message: '文件不存在' }
    }
  } catch (error) {
    return { success: false, message: error.message }
  }
})

// 退出前进行清理
app.on('will-quit', () => {
  // 执行清理操作
})

// 针对macOS，在开发环境下保持激活状态
if (isDevelopment) {
  if (process.platform === 'darwin') {
    app.dock.show()
  }
}