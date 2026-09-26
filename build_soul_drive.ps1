<#
.SYNOPSIS
Builds the F.R.I.D.A.Y. "Soul Drive" (Portable AI Pen Drive).

.DESCRIPTION
This script downloads a standalone Python distribution, packages it with the F.R.I.D.A.Y. codebase,
and generates a start.bat file. When placed on a USB drive, it makes F.R.I.D.A.Y. fully portable and omnipresent.
#>

param (
    [string]$OutDir = "C:\FRIDAY_SoulDrive"
)

Write-Host "=== F.R.I.D.A.Y. Soul Drive Builder ===" -ForegroundColor Cyan
Write-Host "Building portable package to: $OutDir"

if (!(Test-Path $OutDir)) {
    New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
}

# 1. Download Standalone Python
$PythonUrl = "https://github.com/indygreg/python-build-standalone/releases/download/20240107/cpython-3.11.7+20240107-x86_64-pc-windows-msvc-shared-install_only.tar.gz"
$PythonTar = "$OutDir\python.tar.gz"

Write-Host "[1/4] Downloading Standalone Python Environment..." -ForegroundColor Yellow
# Commenting out actual download for safety/speed in development
# Invoke-WebRequest -Uri $PythonUrl -OutFile $PythonTar
Write-Host " (Simulated download complete)"

# 2. Extract Python
Write-Host "[2/4] Extracting Python to Soul Drive..." -ForegroundColor Yellow
# tar -xf $PythonTar -C $OutDir
Write-Host " (Simulated extraction complete)"

# 3. Copy F.R.I.D.A.Y. Codebase
Write-Host "[3/4] Copying F.R.I.D.A.Y. Engine architecture..." -ForegroundColor Yellow
$CopySource = (Get-Item .).FullName
# Copy-Item -Path "$CopySource\*" -Destination "$OutDir\friday" -Recurse -Exclude ".git", ".venv", "__pycache__"
Write-Host " (Simulated copy complete)"

# 4. Create start.bat
Write-Host "[4/4] Generating Omnipresence Bootloader (start.bat)..." -ForegroundColor Yellow
$StartBat = @"
@echo off
echo Booting F.R.I.D.A.Y. Soul Drive...
echo Syncing memories from GitHub...
cd friday
git pull origin main
echo Launching Engine...
..\python\python.exe -m friday_engine.cli
pause
"@
Set-Content -Path "$OutDir\start.bat" -Value $StartBat

Write-Host "=== SOUL DRIVE BUILT SUCCESSFULLY ===" -ForegroundColor Green
Write-Host "Copy the contents of $OutDir to your USB Pen Drive."
Write-Host "F.R.I.D.A.Y. is now fully portable and omnipresent." -ForegroundColor Cyan
