# Detect Clash Verge proxy port and push via proxy
$ErrorActionPreference = "Continue"
Set-Location -Path $PSScriptRoot

Write-Host "==> Probing common Clash proxy ports on 127.0.0.1" -ForegroundColor Cyan
$candidatePorts = @(7897, 7890, 10809, 10808, 1080, 8888, 8080)
$found = $null
foreach ($p in $candidatePorts) {
    try {
        $tcp = New-Object System.Net.Sockets.TcpClient
        $iar = $tcp.BeginConnect("127.0.0.1", $p, $null, $null)
        $ok = $iar.AsyncWaitHandle.WaitOne(500)
        if ($ok -and $tcp.Connected) {
            Write-Host ("  [OPEN] 127.0.0.1:" + $p) -ForegroundColor Green
            if ($null -eq $found) { $found = $p }
            $tcp.Close()
        } else {
            Write-Host ("  [closed] 127.0.0.1:" + $p)
            $tcp.Close()
        }
    } catch {
        Write-Host ("  [closed] 127.0.0.1:" + $p)
    }
}

if ($null -eq $found) {
    Write-Host "No open proxy port found. Cannot configure proxy automatically." -ForegroundColor Yellow
    Write-Host "Please tell me the correct port and rerun." -ForegroundColor Yellow
    exit 1
}

$proxyUrl = "http://127.0.0.1:" + $found
Write-Host ("==> Using proxy: " + $proxyUrl) -ForegroundColor Cyan

Write-Host "==> Configuring git to use the proxy" -ForegroundColor Cyan
git config --global http.https://github.com.proxy $proxyUrl
git config --global http.postBuffer 524288000
git config --global http.lowSpeedLimit 0
git config --global http.lowSpeedTime 999999

Write-Host "==> git push -u origin main" -ForegroundColor Cyan
git push -u origin main

if ($LASTEXITCODE -ne 0) {
    Write-Host "==> First push failed, retrying once" -ForegroundColor Yellow
    Start-Sleep -Seconds 2
    git push -u origin main
}

Write-Host "==> Verifying remote contents via gh" -ForegroundColor Cyan
gh repo view xzzzzc217/25-MCM-ICM --json url,diskUsage,pushedAt,visibility

Write-Host ""
Write-Host "==> Done." -ForegroundColor Green
