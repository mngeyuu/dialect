# 一键：构建 Vue 前端 -> 复制到 pack 目录 -> 打 Windows 包
# 在项目根目录（国创）执行: .\copy-and-pack.ps1

$ErrorActionPreference = "Stop"
$root = $PSScriptRoot

Write-Host "========== 1. 构建 Vue 前端 ==========" -ForegroundColor Cyan
Push-Location (Join-Path $root "dialect-frontend")
npm run build
if ($LASTEXITCODE -ne 0) {
  Pop-Location
  exit 1
}
Pop-Location

Write-Host "`n========== 2. 复制到 pack/dialect-electron-app/build/public ==========" -ForegroundColor Cyan
$dest = Join-Path $root "pack\dialect-electron-app\build\public"
if (Test-Path $dest) {
  Remove-Item -Recurse -Force $dest
}
New-Item -ItemType Directory -Force -Path $dest | Out-Null
Copy-Item -Path (Join-Path $root "dialect-frontend\dist\*") -Destination $dest -Recurse
Write-Host "已复制前端到 $dest"

Write-Host "`n========== 3. 执行 Windows 打包 ==========" -ForegroundColor Cyan
Push-Location (Join-Path $root "pack\dialect-electron-app")
npm run build-win
$packExit = $LASTEXITCODE
Pop-Location

if ($packExit -eq 0) {
  Write-Host "`n完成。安装包在: pack\dialect-electron-app\dist\" -ForegroundColor Green
} else {
  exit $packExit
}
