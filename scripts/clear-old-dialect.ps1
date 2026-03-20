# 清空 public/audio/old_dialect 下所有文件（含 mp3），仅保留 .gitkeep
# 用法：在仓库根目录执行  .\scripts\clear-old-dialect.ps1
# 可选参数：-CorpusWeb 同时清空 corpus-web 下的 old_dialect

param([switch]$CorpusWeb)

$ErrorActionPreference = 'Stop'
$roots = @(
    Join-Path $PSScriptRoot '..\dialect-frontend\public\audio\old_dialect'
)
if ($CorpusWeb) {
    $roots += Join-Path $PSScriptRoot '..\corpus-web\public\audio\old_dialect'
}

foreach ($dir in $roots) {
    $dir = Resolve-Path $dir -ErrorAction SilentlyContinue
    if (-not $dir) { Write-Host "跳过（目录不存在）: $dir"; continue }
    Get-ChildItem -LiteralPath $dir -File -Force | Remove-Item -Force
    $gitkeep = Join-Path $dir '.gitkeep'
    if (-not (Test-Path $gitkeep)) {
        New-Item -ItemType File -Path $gitkeep -Force | Out-Null
    }
    Write-Host "已清空: $dir"
}

Write-Host '完成。'
