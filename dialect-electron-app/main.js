const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const fs = require('fs-extra');
const isDev = require('electron-is-dev');

let mainWindow;
let djangoProcess = null;

// 获取Python可执行文件路径
function getPythonPath() {
  if (isDev) {
    return 'python'; // 开发环境
  } else {
    // 生产环境使用打包的Python
    if (process.platform === 'win32') {
      return path.join(process.resourcesPath, 'python', 'python.exe');
    } else {
      return path.join(process.resourcesPath, 'python', 'bin', 'python');
    }
  }
}

// 启动Django后端
async function startDjangoServer() {
  const pythonPath = getPythonPath();

  // 获取Django项目路径
  const djangoPath = isDev
    ? path.join(__dirname, 'backend')          // 【需修改】如果您的后端目录不是'backend'，请修改
    : path.join(process.resourcesPath, 'backend');

  console.log('启动Django服务器...');
  console.log(`Python路径: ${pythonPath}`);
  console.log(`Django项目路径: ${djangoPath}`);

  // 运行Django服务
  const djangoScript = path.join(djangoPath, 'run_server.py');

  // 在Windows上设置shell: true避免窗口闪现
  djangoProcess = spawn(pythonPath, [djangoScript], {
    cwd: djangoPath,
    shell: process.platform === 'win32'
  });

  // 日志处理
  djangoProcess.stdout.on('data', (data) => {
    console.log(`Django: ${data}`);
  });

  djangoProcess.stderr.on('data', (data) => {
    console.error(`Django错误: ${data}`);
  });

  // 等待Django启动
  return new Promise((resolve) => {
    setTimeout(resolve, 3000);
  });
}

// 创建主窗口
async function createWindow() {
  // 先启动Django
  await startDjangoServer();

  mainWindow = new BrowserWindow({
    width: 1200,                               // 【需修改】可以根据需要调整窗口大小
    height: 800,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    }
  });

  // 加载前端
  const startUrl = isDev
    ? 'http://localhost:8080'                  // 【需修改】如果您的Vue开发服务器端口不是8080，请修改
    : `http://localhost:8000`;

  await mainWindow.loadURL(startUrl);

  if (isDev) {
    mainWindow.webContents.openDevTools();
  }

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

// 处理App生命周期
app.whenReady().then(createWindow);

// 处理Excel文件导入
ipcMain.handle('select-excel-file', async () => {
  const result = await dialog.showOpenDialog({
    properties: ['openFile'],
    filters: [{ name: 'Excel Files', extensions: ['xlsx', 'xls'] }]
  });

  if (!result.canceled && result.filePaths.length > 0) {
    return result.filePaths[0];
  }
  return null;
});

// 应用退出时清理
app.on('will-quit', () => {
  if (djangoProcess) {
    if (process.platform === 'win32') {
      // Windows上需要终止进程树
      spawn('taskkill', ['/pid', djangoProcess.pid, '/f', '/t']);
    } else {
      djangoProcess.kill('SIGTERM');
    }
  }
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});