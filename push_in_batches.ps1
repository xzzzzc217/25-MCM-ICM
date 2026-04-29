# Reset and push in smaller batched commits to avoid GitHub server-side timeout
$ErrorActionPreference = "Continue"
Set-Location -Path $PSScriptRoot

# Use proxy detected earlier
$proxyUrl = "http://127.0.0.1:7897"
git config --global http.https://github.com.proxy $proxyUrl
git config --global http.postBuffer 524288000

Write-Host "==> Resetting commit (keep files in working tree)" -ForegroundColor Cyan
# Drop HEAD entirely so we can rebuild commits from scratch
git update-ref -d HEAD
git rm -r --cached . 2>$null | Out-Null

function Push-Batch {
    param(
        [string]$Message,
        [string[]]$Paths
    )
    Write-Host ""
    Write-Host ("==> Batch: " + $Message) -ForegroundColor Cyan
    foreach ($p in $Paths) {
        if (Test-Path $p) {
            Write-Host ("  add: " + $p)
            git add -- $p
        } else {
            Write-Host ("  skip (missing): " + $p)
        }
    }
    git commit -m $Message
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  (nothing to commit)" -ForegroundColor DarkGray
        return
    }
    git push -u origin main
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  retry push..." -ForegroundColor Yellow
        Start-Sleep -Seconds 3
        git push -u origin main
    }
}

# Batch 1: lightweight bootstrap (README, gitignore, top-level docs and scripts)
Push-Batch -Message "Bootstrap: README, scripts, top-level docs" -Paths @(
    "README.md",
    ".gitignore",
    "main.tex",
    "2023美赛LaTeX模板.txt",
    "setup_github.ps1",
    "verify_push.ps1",
    "push_with_proxy.ps1",
    "push_in_batches.ps1"
)

# Batch 2: 2025 problems (the focus year, ~70MB)
Push-Batch -Message "Add 2025 MCM/ICM official problems and data" -Paths @("2025_MCM-ICM_Problems")

# Batch 3: 25c (current participation work, ~42MB)
Push-Batch -Message "Add 25C: 2025 Problem C solving process" -Paths @("25c")

# Batch 4: 24d (~6MB) and 22c (~39MB) practice rounds
Push-Batch -Message "Add 24d and 22c practice rounds" -Paths @("24d", "22c")

# Batch 5: 2024 archive (~229MB) - largest single batch
Push-Batch -Message "Add 2024 archive: problems and outstanding papers" -Paths @("2024")

# Batch 6: 2023 archive (~154MB)
Push-Batch -Message "Add 2023 archive: problems and outstanding papers" -Paths @("2023")

# Batch 7: remaining loose files (sample papers, code summary, sample zip)
Push-Batch -Message "Add reference papers and code summary" -Paths @(
    "2519836.pdf",
    "美赛.pdf",
    "美赛实例.zip",
    "代码汇总.docx"
)

Write-Host ""
Write-Host "==> All batches pushed. Verifying remote." -ForegroundColor Cyan
gh repo view xzzzzc217/25-MCM-ICM --json url,diskUsage,pushedAt,visibility
git log --oneline

Write-Host ""
Write-Host "==> Done." -ForegroundColor Green
