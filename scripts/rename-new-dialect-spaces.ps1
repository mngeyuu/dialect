# 将 new_dialect 下 mp3 文件名中的下划线 _ 全部改为空格（与「0001 新派 太阳.mp3」格式一致）
#
# 用法示例：
#   powershell -ExecutionPolicy Bypass -File .\scripts\rename-new-dialect-spaces.ps1
#   powershell -ExecutionPolicy Bypass -File .\scripts\rename-new-dialect-spaces.ps1 -CorpusWeb
#   powershell -ExecutionPolicy Bypass -File .\scripts\rename-new-dialect-spaces.ps1 -Path 'D:\...\new_dialect'
param(
    [switch]$CorpusWeb,
    [string[]]$Path
)

$ErrorActionPreference = 'Stop'
if ($Path -and $Path.Count -gt 0) {
    $dirs = $Path
} else {
    $dirs = @(
        Join-Path $PSScriptRoot '..\dialect-frontend\public\audio\new_dialect'
    )
    if ($CorpusWeb) {
        $dirs += Join-Path $PSScriptRoot '..\corpus-web\public\audio\new_dialect'
    }
}

foreach ($dir in $dirs) {
    $dir = Resolve-Path $dir -ErrorAction SilentlyContinue
    if (-not $dir) {
        Write-Host "跳过（目录不存在）"
        continue
    }
    Get-ChildItem -LiteralPath $dir -File -Filter '*.mp3' | ForEach-Object {
        $old = $_.Name
        if ($old -notmatch '_') { return }
        $newName = $old -replace '_', ' '
        $dest = Join-Path $dir $newName
        if (Test-Path -LiteralPath $dest) {
            Write-Warning "已存在同名文件，跳过: $old -> $newName"
            return
        }
        Rename-Item -LiteralPath $_.FullName -NewName $newName
        Write-Host "重命名: $old -> $newName"
    }
    Write-Host "完成目录: $dir"
}
