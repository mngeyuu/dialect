const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

console.log('正在准备打包...');

// 1. 创建一个备份
console.log('备份 Python 环境...');
const pythonEnvPath = path.join(__dirname, 'pack-env');
const backupPath = path.join(__dirname, 'pack-env-backup');

if (fs.existsSync(backupPath)) {
  console.log('删除旧备份...');
  fs.rmdirSync(backupPath, { recursive: true });
}

console.log(`复制环境从 ${pythonEnvPath} 到 ${backupPath}`);
fs.cpSync(pythonEnvPath, backupPath, { recursive: true });

// 2. 创建启动脚本
console.log('创建启动脚本...');
const batchContent = `@echo off
echo 正在启动方言应用...

REM 设置工作目录为当前目录
cd /d "%~dp0"

REM 显示当前目录
echo 当前目录: %CD%

REM 设置环境变量
set PYTHONIOENCODING=utf-8
set PYTHONPATH=%~dp0resources\\backend
set PYTHONHOME=%~dp0resources\\pack-env

REM 启动应用
echo 启动应用主程序...
"%~dp0dialect-app.exe" --enable-logging

REM 应用退出时暂停
echo 应用已退出
if %ERRORLEVEL% NEQ 0 (
  echo 应用异常退出，退出码: %ERRORLEVEL%
  pause
)`;

fs.writeFileSync(path.join(__dirname, 'start-dialect-app.bat'), batchContent);
console.log('启动脚本已创建');

// 3. 清理不必要的文件以减小大小
console.log('清理 Python 环境...');
const foldersToClean = [
  '__pycache__',
  '.git',
  '.github',
  'test',
  'tests',
  'doc',
  'docs',
  'examples'
];

function cleanDir(dir) {
  if (!fs.existsSync(dir)) return;

  const items = fs.readdirSync(dir, { withFileTypes: true });

  for (const item of items) {
    const fullPath = path.join(dir, item.name);

    if (item.isDirectory()) {
      if (foldersToClean.includes(item.name) || item.name.endsWith('.dist-info')) {
        console.log(`删除目录: ${fullPath}`);
        fs.rmdirSync(fullPath, { recursive: true });
      } else {
        cleanDir(fullPath);
      }
    } else if (item.isFile()) {
      if (item.name.endsWith('.pyc') || item.name.endsWith('.pyo')) {
        console.log(`删除文件: ${fullPath}`);
        fs.unlinkSync(fullPath);
      }
    }
  }
}

cleanDir(pythonEnvPath);
console.log('Python 环境清理完成');

console.log('打包前准备工作完成');