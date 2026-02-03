<#
.SYNOPSIS
    调用活字格插件构建器来初始化新项目。

.DESCRIPTION
    此脚本用于自动检测并启动官方的“活字格插件构建器”工具。
    脚本会尝试在常见安装路径下查找构建器，如果找到则直接启动。
    支持传入项目名称参数。

.PARAMETER ProjectName
    要创建的项目名称。如果不提供，默认为 "MyForguncyPlugin"。

.EXAMPLE
    .\InitProject.ps1 -ProjectName "MyNewPlugin"
#>

param(
    [string]$ProjectName = "MyForguncyPlugin"
)

# Define common paths for the builder
$PossiblePaths = @(
    "D:\Code\ForguncyPluginBuilder\forguncyPluginBuilder_V11.1\bin\ForguncyPluginCreator.exe",
    "C:\Program Files\Forguncy Plugin Builder\ForguncyPluginCreator.exe",
    "C:\Program Files (x86)\Forguncy Plugin Builder\ForguncyPluginCreator.exe",
    "$env:LOCALAPPDATA\Forguncy Plugin Builder\ForguncyPluginCreator.exe",
    "E:\forguncyPluginBuilder_V11.1\bin\ForguncyPluginCreator.exe"
)

$BuilderPath = $null

# Check paths
foreach ($path in $PossiblePaths) {
    if (Test-Path $path) {
        $BuilderPath = $path
        break
    }
}

if ($null -eq $BuilderPath) {
    Write-Warning "Forguncy Plugin Builder not found in default paths."
    Write-Host "Checked paths:"
    $PossiblePaths | ForEach-Object { Write-Host " - $_" }
    Write-Host "`nPlease start the builder manually."
    return
}

Write-Host "Builder found: $BuilderPath"
Write-Host "Starting builder for project: $ProjectName ..."

try {
    # Get the directory of the builder executable to set as WorkingDirectory
    # This prevents issues where the builder fails to load resources from relative paths
    $BuilderDir = Split-Path -Parent $BuilderPath
    
    # Try to start the builder with WorkingDirectory set
    Start-Process -FilePath $BuilderPath -WorkingDirectory $BuilderDir -ArgumentList "/name `"$ProjectName`"" -ErrorAction Stop
    
    Write-Host "Builder started. Please complete the project creation in the GUI."
    
    # Logo Generation Prompt
    Write-Host "`nDo you want to generate a professional plugin logo? (Y/N)" -ForegroundColor Yellow
    $response = Read-Host
    if ($response -eq 'Y' -or $response -eq 'y') {
        Write-Host "Select logo icon type:"
        Write-Host "1. Text only (Default)"
        Write-Host "2. Gantt (Industrial/APS)"
        Write-Host "3. Chart (Analytics/Reports)"
        Write-Host "4. Database (Storage/Data)"
        Write-Host "5. Gear (Tools/Processing)"
        $typeIdx = Read-Host "Choice [1-5]"
        $LogoType = switch ($typeIdx) {
            "2" { "gantt" }
            "3" { "chart" }
            "4" { "db" }
            "5" { "gear" }
            Default { "text" }
        }

        $LogoText = Read-Host "Enter 2-3 characters for the logo (e.g. APS)"
        if ([string]::IsNullOrWhiteSpace($LogoText)) { $LogoText = "FP" }
        
        $ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
        $GenerateLogoScript = Join-Path $ScriptDir "generate_logo.py"
        
        # Assume the project is created in the current directory or a subfolder named $ProjectName
        $TargetPath = Join-Path (Get-Location) $ProjectName
        
        if (Test-Path $GenerateLogoScript) {
            # Use --sync to automatically overwrite existing logos
            python $GenerateLogoScript $TargetPath --text $LogoText --type $LogoType --sync
            Write-Host "Logos generated and synchronized in $ProjectName\Resources\" -ForegroundColor Green
            
            Write-Host "`n[Important] For PluginConfig.json (Main Icon), use:" -ForegroundColor Yellow
            Write-Host "Resources/PluginLogo.png (or your custom name)" -ForegroundColor White
            Write-Host "`n[Tip] For Command/CellType class [Icon] attribute, use:" -ForegroundColor Cyan
            Write-Host "[Icon(""pack://application:,,,/$ProjectName;component/Resources/PluginLogo.png"")]" -ForegroundColor White
        } else {
            Write-Warning "Logo generation script not found."
        }
    }

    Write-Host "`nDo you want to add common dependencies (Newtonsoft.Json)? (Y/N)" -ForegroundColor Yellow
    $addJson = Read-Host
    if ($addJson -eq 'Y' -or $addJson -eq 'y') {
        $TargetPath = Join-Path (Get-Location) $ProjectName
        if (Test-Path $TargetPath) {
            Push-Location $TargetPath
            dotnet add package Newtonsoft.Json
            Pop-Location
            Write-Host "Added Newtonsoft.Json to $ProjectName" -ForegroundColor Green
        } else {
            Write-Warning "Project folder $ProjectName not found. Please run 'dotnet add package Newtonsoft.Json' manually later."
        }
    }
}
catch {
    Write-Error "Failed to start builder: $_"
}
