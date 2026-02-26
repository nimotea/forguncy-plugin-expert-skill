<#
.SYNOPSIS
    配置已创建的活字格插件项目（Logo、依赖）。

.DESCRIPTION
    此脚本用于在项目创建完成后，交互式地配置项目：
    1. 生成专业 Logo (SVG + PNG)。
    2. 添加常用 NuGet 依赖 (如 Newtonsoft.Json)。

.PARAMETER ProjectName
    项目名称。如果不提供，默认为 "MyForguncyPlugin"。

.EXAMPLE
    .\setup_project.ps1 -ProjectName "MyNewPlugin"
#>

param(
    [string]$ProjectName = "MyForguncyPlugin"
)

try {
    $TargetPath = Join-Path (Get-Location) $ProjectName
    
    if (-not (Test-Path $TargetPath)) {
        Write-Warning "Project folder '$ProjectName' not found in current directory."
        Write-Warning "Please make sure you have created the project and are running this script from the parent directory."
        return
    }

    # Logo Generation Prompt
    # Removed as per user request (User will explicitly ask for logo generation)
    
    Write-Host "`n=== Plugin Configuration ===" -ForegroundColor Cyan
    Write-Host "`nDo you want to add common dependencies (Newtonsoft.Json)? (Y/N)" -ForegroundColor Yellow
    $addJson = Read-Host
    if ($addJson -eq 'Y' -or $addJson -eq 'y') {
        Push-Location $TargetPath
        dotnet add package Newtonsoft.Json
        Pop-Location
        Write-Host "Added Newtonsoft.Json to $ProjectName" -ForegroundColor Green
    }
    
    Write-Host "`nConfiguration complete!" -ForegroundColor Green
}
catch {
    Write-Error "An error occurred during setup: $_"
}
