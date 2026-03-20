# 打包成 Windows 软件说明

本项目通过 **pack/dialect-electron-app** 将「Vue 前端 + Electron + Django 后端」打成 Windows 安装包（NSIS）或绿色便携版（portable）。

---

## 一、环境要求

- **Node.js**（建议 16+）
- **npm** 或 yarn
- **Python 3**（用于后端；打包时需已生成 `django-server.exe`）
- **Windows 系统**（在 Windows 上打 Windows 包）

---

## 二、打包前准备

### 1. 构建 Vue 前端

在项目根目录执行：

```powershell
cd dialect-frontend
npm install
npm run build
```

默认会生成 `dialect-frontend/dist/`（含 `index.html`、`js/`、`css/` 等）。

### 2. 将前端复制到打包目录

打包程序会从 **pack/dialect-electron-app/build/public/** 读取前端（并随安装包发布）。请把上一步的构建结果复制过去：

```powershell
# 在项目根目录（国创）执行
# 若 build/public 已存在可先删再复制，保证干净
Remove-Item -Recurse -Force pack\dialect-electron-app\build\public -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force pack\dialect-electron-app\build\public
Copy-Item -Path dialect-frontend\dist\* -Destination pack\dialect-electron-app\build\public -Recurse
```

或使用提供的脚本（见下一节）。

### 3. 确认 Django 后端可执行文件

打包时需要 **pack/dialect-electron-app/resources/django-server.exe**（由 Django 项目用 PyInstaller 等打成 exe）。  
若还没有：

- 在 **pack/dialect-electron-app/backend** 用 PyInstaller 等工具将 Django 启动逻辑打成 `django-server.exe`
- 将生成的 `django-server.exe` 放到 **pack/dialect-electron-app/resources/** 下

若已有该文件，无需再生成。

### 4. 其他资源（可选）

- **pack/dialect-electron-app/backend/**：Django 后端代码与配置（打包会拷贝）
- **pack/dialect-electron-app/pack-env/**：Python 虚拟环境或依赖（打包会拷贝）
- **pack/dialect-electron-app/audio/**：若有 MP3 等音频资源，会拷贝到 `backend/audio`

---

## 三、执行打包

进入打包目录并安装依赖、执行 Windows 打包：

```powershell
cd pack\dialect-electron-app
npm install
npm run build-win
```

或使用「先执行 prepackage 再打包」的脚本：

```powershell
npm run package
```

打包完成后，输出在 **pack/dialect-electron-app/dist/**：

- **方言档案 Setup x.x.x.exe**：NSIS 安装包（可指定安装路径、创建快捷方式）
- **方言档案 x.x.x.exe**：绿色便携版，无需安装

---

## 四、一键复制前端并打包（推荐）

在项目根目录可使用以下脚本，先构建前端、复制到 **build/public**，再打 Windows 包。

**copy-and-pack.ps1**（放在项目根目录）：

```powershell
# 在项目根目录执行
Set-Location $PSScriptRoot

Write-Host "1. 构建 Vue 前端..."
Set-Location dialect-frontend
npm run build
if ($LASTEXITCODE -ne 0) { exit 1 }
Set-Location ..

Write-Host "2. 复制到 pack/dialect-electron-app/build/public..."
$dest = "pack\dialect-electron-app\build\public"
Remove-Item -Recurse -Force $dest -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force $dest
Copy-Item -Path dialect-frontend\dist\* -Destination $dest -Recurse

Write-Host "3. 执行 Windows 打包..."
Set-Location pack\dialect-electron-app
npm run build-win
Set-Location $PSScriptRoot
Write-Host "完成。安装包在 pack\dialect-electron-app\dist\"
```

在 PowerShell 中执行：

```powershell
.\copy-and-pack.ps1
```

---

## 五、常见问题

| 现象 | 处理 |
|------|------|
| 打包时提示找不到 `django-server.exe` | 确认 **resources/django-server.exe** 已存在并参与打包（见 package.json 的 extraResources） |
| 安装后打开是白屏或“找不到前端文件” | 确认已把 **dialect-frontend/dist/** 复制到 **build/public/** 后再执行打包 |
| Electron 下载慢或失败 | 可配置 npm 镜像；或使用 package.json 里已有的 **electronDownload.cache** 指向本地已下载的 Electron |
| prepackage 报错（如 pack-env 不存在） | 确保 **pack-env** 目录存在；若不需要可暂时注释 prepackage 中的相关步骤，仅执行 `npm run build-win` |

---

## 六、打包产物说明

- **dist/win-unpacked/**：未打成安装包的绿色版，可直接运行其中的 exe 做测试。
- **dist/*.exe**：给用户分发的安装包或便携版。

安装后，应用会启动内嵌的 Django 服务并打开 Electron 窗口加载前端；数据与日志路径在用户目录下（如 `%APPDATA%` 对应目录）。
