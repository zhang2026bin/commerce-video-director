# 安装 带货视频导演台 到 DSH
param(
    [string]$Profile = "desktop"
)

$ErrorActionPreference = "Stop"
$repo = $PSScriptRoot
$package = "dsh-agent-commerce-video"
$patch = Join-Path $repo "plugin\cordis.patch.yml"
$agentDir = Join-Path $repo "agent"
$enc = New-Object System.Text.UTF8Encoding($false)

if (-not (Test-Path $patch)) { throw "找不到 $patch" }

# 1. 改写 preset 里的绝对路径
Copy-Item $patch "$patch.bak" -Force
$text = Get-Content $patch -Raw -Encoding UTF8
$text = [regex]::Replace($text, '[A-Za-z]:\\[^\r\n]*?\\agents\\commerce-video\\', ($agentDir.TrimEnd('\') + '\'))
[IO.File]::WriteAllText($patch, $text, $enc)
Write-Host "[1/4] 已改写 preset 路径 -> $agentDir"

# 2. 安装技能
$skillSrc = Join-Path $repo "skill"
if (Test-Path $skillSrc) {
    $skillDst = Join-Path $env:USERPROFILE ".agents\skills\ai-commerce-director"
    Copy-Item $skillSrc $skillDst -Recurse -Force
    Write-Host "[2/4] 技能已安装 -> $skillDst"
}

# 3. 安装插件
if (-not (Get-Command dsh -ErrorAction SilentlyContinue)) {
    throw "找不到 dsh 命令，请确认 DeepSeek Harness 已安装并在 PATH 中"
}
& dsh plugin --profile $Profile add "file:$(Join-Path $repo 'plugin')"
if ($LASTEXITCODE -ne 0) { throw "dsh plugin add 失败" }
Write-Host "[3/4] 插件已安装"

# 4. 加入 bundle 列表
$profileJson = Join-Path $env:USERPROFILE ".dsh\profiles\$Profile\package.json"
if (Test-Path $profileJson) {
    $data = Get-Content $profileJson -Raw -Encoding UTF8 | ConvertFrom-Json
    if ($data.dsh.profile.bundles -notcontains $package) {
        $data.dsh.profile.bundles = @($data.dsh.profile.bundles) + $package
        [IO.File]::WriteAllText($profileJson, ($data | ConvertTo-Json -Depth 10), $enc)
        Write-Host "[4/4] 已加入 bundles: $package"
    } else {
        Write-Host "[4/4] bundles 已包含 $package"
    }
} else {
    Write-Host "[4/4] 未找到 $profileJson，请手动把 $package 加进 dsh.profile.bundles"
}

Write-Host ""
Write-Host "完成。重启 DeepSeek Harness，在 Agent 列表选择 commerce-video。" -ForegroundColor Green
