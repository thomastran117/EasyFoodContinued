$ErrorActionPreference = "Stop"

$ScriptDir =
    if ($PSScriptRoot) {
        $PSScriptRoot
    } else {
        Split-Path -Parent $MyInvocation.MyCommand.Definition
    }

$RepoRoot = Resolve-Path (Join-Path $ScriptDir "..\..")

Set-Location $RepoRoot

Write-Host "Building and starting containers (detached)..." -ForegroundColor Cyan
docker compose up -d --build

Write-Host "`nSwitching to attached mode..." -ForegroundColor Cyan
docker compose up

Write-Host ""
Write-Host "All services are now running." -ForegroundColor Green
Write-Host "Frontend: http://localhost:3040"
Write-Host "Backend : http://localhost:8040"
