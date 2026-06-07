# Firebase login + deploy helper for Windows (PowerShell)
# Usage:
#   .\scripts\firebase-windows.ps1              # login + verify project
#   .\scripts\firebase-windows.ps1 -Deploy      # login check + build + deploy
#   .\scripts\firebase-windows.ps1 -LoginOnly   # only firebase login
#   .\scripts\firebase-windows.ps1 -CiToken     # print CI token for GitHub Actions

param(
    [switch]$LoginOnly,
    [switch]$Deploy,
    [switch]$CiToken
)

$ErrorActionPreference = "Stop"
$ProjectId = "hotel-restaurant-minimart"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root

function Write-Step($msg) { Write-Host "`n==> $msg" -ForegroundColor Cyan }
function Write-Ok($msg)   { Write-Host "OK: $msg" -ForegroundColor Green }
function Write-Warn($msg) { Write-Host "WARN: $msg" -ForegroundColor Yellow }
function Write-Err($msg)  { Write-Host "ERROR: $msg" -ForegroundColor Red; exit 1 }

Write-Host ""
Write-Host "HotelRestaurantMini-Mart — Firebase setup (Windows)" -ForegroundColor White
Write-Host "Project: $ProjectId" -ForegroundColor Gray
Write-Host "Account: use roi.reuven@gmail.com when the browser opens" -ForegroundColor Gray
Write-Host ""

# Node.js
Write-Step "Checking Node.js..."
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Err "Node.js not found. Install from https://nodejs.org/ (LTS 18+) then run this script again."
}
$nodeVer = node -v
Write-Ok "Node $nodeVer"

# Python (needed for app patches)
Write-Step "Checking Python..."
$python = $null
foreach ($cmd in @("python", "py", "python3")) {
    if (Get-Command $cmd -ErrorAction SilentlyContinue) { $python = $cmd; break }
}
if (-not $python) {
    Write-Warn "Python not found. Install from https://python.org/downloads/ (check Add to PATH)."
    if ($Deploy) { Write-Err "Cannot deploy without Python (app patch scripts)." }
} else {
    Write-Ok "Python found ($python)"
}

# Git Bash optional (build uses Node.js)

# npm install
Write-Step "Installing npm dependencies..."
npm install
if ($LASTEXITCODE -ne 0) { Write-Err "npm install failed." }
Write-Ok "Dependencies installed"

# Firebase login
if ($CiToken) {
    Write-Step "Generating CI token (for GitHub FIREBASE_TOKEN secret)..."
    Write-Host "Sign in as roi.reuven@gmail.com when prompted." -ForegroundColor Yellow
    npx firebase login:ci
    if ($LASTEXITCODE -ne 0) { Write-Err "firebase login:ci failed." }
    Write-Ok "Copy the token above into GitHub: Settings -> Secrets -> Actions -> FIREBASE_TOKEN"
    exit 0
}

Write-Step "Firebase login (browser will open)..."
Write-Host "Choose Google account: roi.reuven@gmail.com" -ForegroundColor Yellow
npx firebase login
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Warn "If the browser did not open, try:"
    Write-Host "  npx firebase login --no-localhost" -ForegroundColor White
    Write-Err "firebase login failed."
}
Write-Ok "Logged in to Firebase"

if ($LoginOnly) {
    Write-Ok "Login complete. Run with -Deploy when ready to upload."
    exit 0
}

# Verify project access
Write-Step "Listing Firebase projects..."
npx firebase projects:list
if ($LASTEXITCODE -ne 0) { Write-Err "Cannot list projects. Check account permissions for $ProjectId." }

Write-Step "Selecting project $ProjectId..."
npx firebase use $ProjectId
if ($LASTEXITCODE -ne 0) { Write-Err "Cannot use project $ProjectId." }
Write-Ok "Project $ProjectId selected"

if (-not $Deploy) {
    Write-Host ""
    Write-Ok "Firebase is connected."
    Write-Host "To deploy app + documentation, run:" -ForegroundColor White
    Write-Host "  .\scripts\firebase-windows.ps1 -Deploy" -ForegroundColor Yellow
    Write-Host "  or double-click: firebase-fix.bat deploy" -ForegroundColor Yellow
    exit 0
}

# Build + deploy
Write-Step "Building app + documentation..."
npm run build
if ($LASTEXITCODE -ne 0) { Write-Err "Build failed." }
Write-Ok "Build complete"

Write-Step "Verifying bundle..."
npm run verify
if ($LASTEXITCODE -ne 0) { Write-Err "Verify failed." }
Write-Ok "Bundle verified"

Write-Step "Deploying to Firebase Hosting..."
npx firebase deploy --only hosting --project $ProjectId
if ($LASTEXITCODE -ne 0) { Write-Err "Deploy failed." }

Write-Host ""
Write-Ok "Deploy finished!"
Write-Host "Live app:  https://hotel-restaurant-minimart.firebaseapp.com/" -ForegroundColor Green
Write-Host "Docs:      https://hotel-restaurant-minimart.firebaseapp.com/doc/" -ForegroundColor Green
Write-Host "Hard refresh the app (Ctrl+Shift+R) to see Documentation in the menu." -ForegroundColor Gray
