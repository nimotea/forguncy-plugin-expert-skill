<#
.SYNOPSIS
    调用 Python 脚本打包指定 Skill。

.DESCRIPTION
    此脚本用于简化打包流程，调用 scripts/package_skill.py。
    它将生成一个符合 npx skills 标准的分发包结构。

.PARAMETER SkillName
    要打包的 Skill 名称（位于 src/skills/ 下）或路径。默认为 forguncy-plugin-expert。

.EXAMPLE
    .\scripts\package_skill.ps1
    .\scripts\package_skill.ps1 -SkillName my-new-skill
#>

param (
    [string]$SkillName = "forguncy-plugin-expert"
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$RepoRoot = Split-Path -Parent $ScriptDir
$PythonScript = Join-Path $ScriptDir "package_skill.py"

Write-Host "Repo Root: $RepoRoot"
Write-Host "Packager Script: $PythonScript"
Write-Host "Target Skill: $SkillName"

if (-not (Test-Path $PythonScript)) {
    Write-Error "Cannot find package_skill.py at $PythonScript"
    exit 1
}

# Check if python is available
try {
    python --version | Out-Null
} catch {
    Write-Error "Python is not installed or not in PATH."
    exit 1
}

# Define output directory (build folder at repo root)
$OutputDir = Join-Path $RepoRoot "build"

Write-Host "Building skill distribution to: $OutputDir"

# Run the python script to build the folder structure
# 注意：这里直接传递 SkillName，Python 脚本会根据它去 src/skills/ 下查找
python $PythonScript $SkillName --output $OutputDir --format folder

if ($LASTEXITCODE -eq 0) {
    Write-Host "Build completed successfully."
    Write-Host "You can now verify this build locally using:"
    Write-Host "npx skills add $OutputDir --skill $SkillName"
} else {
    Write-Error "Build failed."
    exit $LASTEXITCODE
}
