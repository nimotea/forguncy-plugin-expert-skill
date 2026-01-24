param(
    [Parameter(Mandatory=$true)]
    [string]$TargetForguncyPath
)

$ErrorActionPreference = "Stop"

function Get-ForguncyLibPath {
    param([string]$BasePath)
    
    $candidates = @(
        $BasePath,
        (Join-Path $BasePath "Website\bin"),
        (Join-Path $BasePath "Bin")
    )

    foreach ($path in $candidates) {
        if (Test-Path (Join-Path $path "GrapeCity.Forguncy.ServerApi.dll")) {
            return $path
        }
    }
    return $null
}

function Get-ForguncyExecutablePath {
    param([string]$BasePath)
    
    # Try to find Forguncy.Console.exe (common for debugging)
    $consoleExe = Join-Path $BasePath "Forguncy.Console.exe"
    if (Test-Path $consoleExe) { return $consoleExe }

    # Fallback to Designer? Or maybe user provided the Designer folder directly
    $designerExe = Join-Path $BasePath "ForguncyDesigner.exe"
    if (Test-Path $designerExe) { return $designerExe }

    return $null
}

Write-Host "Verifying Forguncy Path: $TargetForguncyPath"

if (-not (Test-Path $TargetForguncyPath)) {
    Write-Error "Path not found: $TargetForguncyPath"
}

$libPath = Get-ForguncyLibPath -BasePath $TargetForguncyPath
if (-not $libPath) {
    Write-Warning "Could not find 'GrapeCity.Forguncy.ServerApi.dll' in typical subdirectories of $TargetForguncyPath."
    Write-Warning "Will assume $TargetForguncyPath is the intended library path, but please verify."
    $libPath = $TargetForguncyPath
} else {
    Write-Host "Found libraries at: $libPath"
}

$execPath = Get-ForguncyExecutablePath -BasePath $TargetForguncyPath
if ($execPath) {
    Write-Host "Found executable at: $execPath"
}

# 1. Update .csproj files
$csprojFiles = Get-ChildItem -Filter "*.csproj" -Recurse
foreach ($csproj in $csprojFiles) {
    Write-Host "Processing $($csproj.Name)..."
    [xml]$xml = Get-Content $csproj.FullName
    $ns = @{ ns = $xml.Project.NamespaceURI }
    $changed = $false

    # Find Reference nodes with HintPath
    # Note: .NET Core SDK csproj might not have namespace in root, handling both
    $references = $xml.SelectNodes("//Reference") 
    if (-not $references) {
        $references = $xml.SelectNodes("//ns:Reference", $ns)
    }

    foreach ($ref in $references) {
        $hintPathNode = $ref.SelectSingleNode("HintPath")
        if (-not $hintPathNode) { 
            $hintPathNode = $ref.SelectSingleNode("ns:HintPath", $ns) 
        }

        # Updated Logic: 
        # 1. Match "GrapeCity.Forguncy" OR "Forguncy." (to catch Forguncy.Log, Forguncy.Commands etc.)
        # 2. Check if the DLL exists in the target lib path. If yes, update it.
        $dllName = Split-Path $hintPathNode.InnerText -Leaf
        if ($hintPathNode -and ($hintPathNode.InnerText -match "GrapeCity.Forguncy" -or $hintPathNode.InnerText -match "Forguncy\.")) {
            
            $potentialNewPath = Join-Path $libPath $dllName
            $finalPath = $null

            # 1. Check primary lib path (Website\bin)
            if (Test-Path $potentialNewPath) {
                $finalPath = $potentialNewPath
            } else {
                # 2. Check designerBin path (Website\designerBin)
                # This handles design-time DLLs like GrapeCity.Forguncy.CellTypes.Design.dll
                $parentPath = Split-Path $libPath -Parent
                $designerPath = Join-Path $parentPath "designerBin"
                $potentialDesignerPath = Join-Path $designerPath $dllName
                
                if (Test-Path $potentialDesignerPath) {
                    $finalPath = $potentialDesignerPath
                }
            }

            # Only update if the target DLL actually exists in one of the Forguncy folders
            # This prevents breaking references to local/nuget DLLs that happen to have "Forguncy" in the name but aren't core libs
            if ($finalPath) {
                 if ($hintPathNode.InnerText -ne $finalPath) {
                    Write-Host "  Updating reference: $dllName -> $finalPath"
                    $hintPathNode.InnerText = $finalPath
                    $changed = $true
                }
            } else {
                 Write-Warning "  Skipping $dllName : Not found in target library path ($libPath) or designerBin"
            }
        }
    }

    if ($changed) {
        $xml.Save($csproj.FullName)
        Write-Host "  Saved changes to $($csproj.Name)"
    }
}

# 2. Update launchSettings.json
$launchSettingsFiles = Get-ChildItem -Filter "launchSettings.json" -Recurse
foreach ($file in $launchSettingsFiles) {
    Write-Host "Processing $($file.Name)..."
    $content = Get-Content $file.FullName -Raw
    
    try {
        $jsonObj = ConvertFrom-Json $content
        $changed = $false
        
        if ($jsonObj.profiles) {
            foreach ($profileName in $jsonObj.profiles.PSObject.Properties.Name) {
                $profile = $jsonObj.profiles.$profileName
                if ($profile.executablePath -and $profile.executablePath -match "Forguncy") {
                     if ($execPath -and $profile.executablePath -ne $execPath) {
                        $profile.executablePath = $execPath
                        $changed = $true
                     }
                }
            }
        }
        
        if ($changed) {
            $newContent = $jsonObj | ConvertTo-Json -Depth 10
            Set-Content -Path $file.FullName -Value $newContent
            Write-Host "  Updated executablePath in $($file.Name)"
        }
    } catch {
        Write-Warning "Failed to parse or update $($file.Name): $_"
    }
}

Write-Host "Update complete."
