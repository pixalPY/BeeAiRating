# PowerShell script to add Git to PATH
Write-Host "Checking for Git installation..." -ForegroundColor Yellow

$gitPaths = @(
    "C:\Program Files\Git\bin",
    "C:\Program Files (x86)\Git\bin",
    "C:\Git\bin"
)

$gitFound = $false
$gitPath = ""

foreach ($path in $gitPaths) {
    if (Test-Path $path) {
        $gitFound = $true
        $gitPath = $path
        Write-Host "Git found at: $path" -ForegroundColor Green
        break
    }
}

if (-not $gitFound) {
    Write-Host "Git not found in common locations." -ForegroundColor Red
    Write-Host "Please install Git from: https://git-scm.com/download/win" -ForegroundColor Yellow
    Write-Host "Make sure to select 'Git from the command line and also from 3rd-party software' during installation." -ForegroundColor Yellow
    exit 1
}

# Check if Git is already in PATH
$currentPath = [Environment]::GetEnvironmentVariable("Path", "Machine")
if ($currentPath -like "*$gitPath*") {
    Write-Host "Git is already in PATH!" -ForegroundColor Green
} else {
    Write-Host "Adding Git to PATH..." -ForegroundColor Yellow
    $newPath = $currentPath + ";" + $gitPath
    [Environment]::SetEnvironmentVariable("Path", $newPath, "Machine")
    Write-Host "Git added to PATH. Please restart your terminal and try again." -ForegroundColor Green
}

Write-Host "Current PATH entries:" -ForegroundColor Cyan
$currentPath.Split(';') | Where-Object { $_ -like "*git*" -or $_ -like "*Git*" } | ForEach-Object { Write-Host "  $_" } 