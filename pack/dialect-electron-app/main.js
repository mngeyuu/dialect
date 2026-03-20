const { app, BrowserWindow, dialog } = require('electron');
const path = require('path');
const fs = require('fs');
const { spawn } = require('child_process');

// 处理未捕获的异常
process.on('uncaughtException', (error) => {
  console.error('未捕获的异常:', error);
});

// 处理未处理的 Promise 拒绝
process.on('unhandledRejection', (reason, promise) => {
  console.error('未处理的 Promise 拒绝:', reason);
});

// 保存 Django 服务器进程的引用
let djangoProcess = null;

// 获取资源路径
function getResourcePath() {
  return app.isPackaged ? process.resourcesPath : path.join(__dirname, 'resources');
}

// 启动 Django 服务器
function startDjangoServer() {
  try {
    console.log('准备启动 Django 服务器...');

    const resourcePath = getResourcePath();

    // 定位打包的 Django 服务器可执行文件
    const djangoServerPath = path.join(resourcePath, 'django-server.exe');
    console.log('Django 服务器路径:', djangoServerPath);

    // 检查文件是否存在
    if (!fs.existsSync(djangoServerPath)) {
      console.error(`错误: Django 服务器不存在: ${djangoServerPath}`);
      dialog.showErrorBox(
        'Django 错误',
        `找不到 Django 服务器: ${djangoServerPath}\n应用可能无法正常工作。`
      );
      return;
    }

    // 确保临时目录存在
    const tempDir = path.join(app.getPath('userData'), 'temp');
    if (!fs.existsSync(tempDir)) {
      fs.mkdirSync(tempDir, { recursive: true });
    }

    // 创建日志目录
    const logDir = path.join(app.getPath('userData'), 'logs');
    if (!fs.existsSync(logDir)) {
      fs.mkdirSync(logDir, { recursive: true });
    }

    // 启动独立的 Django 进程
    console.log('启动 Django 服务器...');
    djangoProcess = spawn(djangoServerPath, [], {
      env: {
        ...process.env,
        TEMP: tempDir,
        TMP: tempDir,
        APPDATA: app.getPath('userData')
      },
      stdio: 'pipe',
      windowsHide: false
    });

    if (!djangoProcess) {
      console.error('错误: 无法创建 Django 进程!');
      return;
    }

    console.log('Django 进程已启动, PID:', djangoProcess.pid);

    // 设置输出编码
    djangoProcess.stdout.setEncoding('utf-8');
    djangoProcess.stderr.setEncoding('utf-8');

    // 处理输出
    djangoProcess.stdout.on('data', (data) => {
      console.log('Django:', data.toString().trim());
    });

    djangoProcess.stderr.on('data', (data) => {
      console.error('Django 错误:', data.toString().trim());
    });

    // 处理事件
    djangoProcess.on('error', (error) => {
      console.error('Django 进程错误:', error);
      dialog.showErrorBox('Django 错误', `启动 Django 时出错: ${error.message}`);
    });

    djangoProcess.on('close', (code) => {
      console.log(`Django 服务器进程已关闭，退出码 ${code}`);
      if (code !== 0 && code !== null) {
        const logFile = path.join(app.getPath('userData'), 'logs', 'django-server.log');
        let errorDetail = `请检查日志文件获取详细信息: ${logFile}`;

        // 尝试读取最后的日志内容
        try {
          if (fs.existsSync(logFile)) {
            const logContent = fs.readFileSync(logFile, 'utf-8');
            const lastLines = logContent.split('\n').slice(-10).join('\n');
            errorDetail = `最近的日志信息:\n${lastLines}\n\n${errorDetail}`;
          }
        } catch (err) {
          console.error('读取日志文件时出错:', err);
        }

        dialog.showMessageBox({
          type: 'error',
          title: 'Django 服务器错误',
          message: `Django 进程意外退出，退出码: ${code}`,
          detail: errorDetail,
          buttons: ['查看日志', '忽略'],
          defaultId: 0
        }).then(result => {
          if (result.response === 0) {
            // 打开日志文件
            require('electron').shell.openPath(logFile);
          }
        });
      }
      djangoProcess = null;
    });

  } catch (error) {
    console.error('Django 启动过程中出错:', error);
    dialog.showErrorBox('Django 启动失败', `启动 Django 服务器时出错: ${error.message}`);
  }
}

// 等待 Django 服务器准备就绪
function waitForDjango(maxAttempts = 30, interval = 1000) {
  return new Promise((resolve) => {
    let attempts = 0;

    const checkServer = () => {
      const request = require('http').request({
        method: 'GET',
        hostname: 'localhost',
        port: 8000,
        path: '/',
        timeout: 1000
      }, (response) => {
        if (response.statusCode === 200) {
          console.log('Django 服务器已就绪');
          resolve(true);
        } else {
          retry();
        }
      });

      request.on('error', () => {
        retry();
      });

      request.end();
    };

    const retry = () => {
      attempts++;
      if (attempts >= maxAttempts) {
        console.error(`Django 服务器在 ${maxAttempts} 次尝试后仍未就绪`);
        resolve(false);
      } else {
        setTimeout(checkServer, interval);
      }
    };

    checkServer();
  });
}

let mainWindow;

async function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
      webSecurity: false
    }
  });

  // 配置跨域请求处理
  mainWindow.webContents.session.webRequest.onBeforeSendHeaders(
    { urls: ['http://localhost:8000/*'] },
    (details, callback) => {
      details.requestHeaders['Origin'] = 'http://localhost:8000';
      callback({ requestHeaders: details.requestHeaders });
    }
  );

  // 加载前端：打包后从 resources/public/ 加载，开发时从 build/ 加载
  const resourcePath = getResourcePath();
  const frontendPath = app.isPackaged
    ? path.join(resourcePath, 'public', 'index.html')
    : path.join(__dirname, 'build', 'index.html');
  console.log('加载前端文件:', frontendPath);

  if (!fs.existsSync(frontendPath)) {
    console.error(`错误: 找不到前端文件: ${frontendPath}`);
    await mainWindow.loadURL('data:text/html;charset=utf-8,<h1>错误</h1><p>找不到前端文件，请先构建前端并复制到 build/public/ 再打包。</p>');
    return;
  }

  try {
    await mainWindow.loadFile(frontendPath);
    console.log('前端加载成功');
  } catch (error) {
    console.error('加载前端时出错:', error);
    await mainWindow.loadURL('data:text/html;charset=utf-8,<h1>错误</h1><p>加载前端时出错</p>');
  }

  mainWindow.on('closed', function () {
    mainWindow = null;
  });
}

app.whenReady().then(async () => {
  console.log('Electron 应用已准备好，开始初始化...');

  // 首先启动 Django 服务器
  console.log('准备启动 Django 服务器...');
  startDjangoServer();

  // 等待 Django 服务器就绪
  console.log('等待 Django 服务器就绪...');
  const isReady = await waitForDjango();

  if (!isReady) {
    dialog.showMessageBox({
      type: 'warning',
      title: 'Django 服务器警告',
      message: 'Django 服务器可能未正确启动。应用的某些功能可能无法工作。',
      buttons: ['继续']
    });
  }

  // 创建窗口
  console.log('准备创建 Electron 窗口...');
  createWindow();

  app.on('activate', function () {
    if (mainWindow === null) createWindow();
  });
});

app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') app.quit();
});

app.on('will-quit', () => {
  // 关闭 Django 服务器
  if (djangoProcess) {
    console.log('正在关闭 Django 服务器...');
    try {
      if (process.platform === 'win32') {
        spawn('taskkill', ['/pid', djangoProcess.pid, '/f', '/t'], { shell: true });
      } else {
        djangoProcess.kill();
      }
    } catch (error) {
      console.error('关闭 Django 服务器时出错:', error);
    }
  }
});