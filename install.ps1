Write-Host "=========================================================" -ForegroundColor Cyan
Write-Host "             F.R.I.D.A.Y. ONE-LINE DEPLOYMENT" -ForegroundColor Cyan
Write-Host "=========================================================" -ForegroundColor Cyan

# 1. Check for Git
if (!(Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Error "❌ Git is not installed. Please install Git for Windows first."
    exit
}

# 2. Clone the repository
$TargetDir = "FRIDAY"
if (Test-Path $TargetDir) {
    Write-Host "⚠️ Directory '$TargetDir' already exists. Updating via git pull..." -ForegroundColor Yellow
    Set-Location $TargetDir
    git pull
} else {
    Write-Host "🚀 Cloning F.R.I.D.A.Y. repository..." -ForegroundColor Green
    # Replace <USERNAME>/<REPO> with the actual Github URL once uploaded
    git clone https://github.com/YOUR_USERNAME/FRIDAY.git $TargetDir
    Set-Location $TargetDir
}

# 3. Detect Python and run the universal installer
Write-Host "📦 Bootstrapping dependencies..." -ForegroundColor Green
if (Get-Command python -ErrorAction SilentlyContinue) {
    python install.py
} else {
    Write-Error "❌ Python is not installed or not in PATH. Please install Python."
    exit
}

Write-Host "✅ Deployment successful. You are currently in the $TargetDir directory." -ForegroundColor Green
