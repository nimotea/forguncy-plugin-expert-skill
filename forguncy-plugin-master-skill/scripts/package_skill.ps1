<#
.SYNOPSIS
    调用 Python 脚本打包当前 Skill。

.DESCRIPTION
    此脚本用于简化打包流程，自动定位当前 Skill 根目录并调用 scripts/package_skill.py。
    生成的 .skill 文件将位于上一级目录（或指定目录）。

.EXAMPLE
    .\scripts\package_skill.ps1
#>

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$SkillRoot = Split-Path -Parent $ScriptDir
$PythonScript = Join-Path $ScriptDir "package_skill.py"

Write-Host "Skill Root: $SkillRoot"
Write-Host "Packager Script: $PythonScript"

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

# Run the python script
# Output to the parent directory of the skill root to avoid packaging the package itself if run recursively (though logic handles excludes)
# Or just output to current dir.
# Let's output to the skill root's parent to simulate a "build" artifact.
$OutputDir = Split-Path -Parent $SkillRoot

Write-Host "Packaging skill..."
python $PythonScript $SkillRoot $OutputDir
