# One-shot script to host this folder on GitHub
# Usage: .\setup_github.ps1
# Requires: git and gh CLI installed and authenticated

$ErrorActionPreference = "Stop"

$RepoName = "25-MCM-ICM"
$RepoDesc = "MCM/ICM archive: past problems (2023, 2024), 2025 problems and 25C full solving process"
$Visibility = "public"   # change to "private" for a private repo
$DefaultBranch = "main"

Write-Host "==> cd to project folder" -ForegroundColor Cyan
Set-Location -Path $PSScriptRoot

Write-Host "==> Cleaning macOS junk files (__MACOSX, .DS_Store, ._*)" -ForegroundColor Cyan
Get-ChildItem -Path . -Recurse -Force -Directory -Filter "__MACOSX" -ErrorAction SilentlyContinue | ForEach-Object {
    Write-Host ("  rm dir: " + $_.FullName)
    Remove-Item -LiteralPath $_.FullName -Recurse -Force -ErrorAction SilentlyContinue
}
Get-ChildItem -Path . -Recurse -Force -File -ErrorAction SilentlyContinue | Where-Object {
    $_.Name -eq ".DS_Store" -or $_.Name -like "._*"
} | ForEach-Object {
    Write-Host ("  rm file: " + $_.FullName)
    Remove-Item -LiteralPath $_.FullName -Force -ErrorAction SilentlyContinue
}

Write-Host "==> Cleaning any leftover .git directory" -ForegroundColor Cyan
if (Test-Path ".git") {
    Get-ChildItem -Path ".git" -Recurse -Force -ErrorAction SilentlyContinue | ForEach-Object {
        try { $_.Attributes = "Normal" } catch {}
    }
    Remove-Item -LiteralPath ".git" -Recurse -Force
}

Write-Host "==> git init -b $DefaultBranch" -ForegroundColor Cyan
git init -b $DefaultBranch

Write-Host "==> set core.quotepath false (display CJK filenames correctly)" -ForegroundColor Cyan
git config core.quotepath false

Write-Host "==> git add -A" -ForegroundColor Cyan
git add -A

Write-Host "==> git commit" -ForegroundColor Cyan
git commit -m "Initial commit: MCM/ICM archive and 25C solving process"

Write-Host "==> Checking gh auth status" -ForegroundColor Cyan
gh auth status
if ($LASTEXITCODE -ne 0) {
    Write-Host "Not logged in. Please run: gh auth login" -ForegroundColor Yellow
    exit 1
}

Write-Host "==> gh repo create + push (visibility: $Visibility)" -ForegroundColor Cyan
gh repo create $RepoName "--$Visibility" --source=. --remote=origin --description $RepoDesc --push

Write-Host ""
Write-Host "==> Done." -ForegroundColor Green
$url = (gh repo view --json url -q .url)
Write-Host ("Repo URL: " + $url)
