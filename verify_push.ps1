# Verify and retry push
$ErrorActionPreference = "Continue"
Set-Location -Path $PSScriptRoot

# Increase HTTP buffer to help with large pushes (Chinese network often unstable)
git config http.postBuffer 524288000
git config http.lowSpeedLimit 0
git config http.lowSpeedTime 999999

Write-Host "==> git remote -v" -ForegroundColor Cyan
git remote -v

Write-Host "==> git status" -ForegroundColor Cyan
git status

Write-Host "==> git push (retry)" -ForegroundColor Cyan
git push -u origin main

Write-Host "==> Verifying remote contents via gh" -ForegroundColor Cyan
gh repo view xzzzzc217/25-MCM-ICM --json url,diskUsage,pushedAt,visibility

Write-Host "==> Done." -ForegroundColor Green
