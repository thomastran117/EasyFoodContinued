[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"

try {
  $nodeVersion = & node -v
  $npmVersion  = & npm -v
  Write-Host "Node: $nodeVersion  npm: $npmVersion" -ForegroundColor Green
} catch {
  throw "Node.js (and npm) are not installed or not on PATH."
}

try {
  $pythonVersion = & python --version 2>$null
  Write-Host "Python: $pythonVersion" -ForegroundColor Green
} catch {
  throw "Python is not installed or not on PATH."
}

$RootDir     = Resolve-Path (Join-Path $PSScriptRoot "..")
$FrontendDir = Resolve-Path (Join-Path $RootDir "frontend")
$BackendDir  = Resolve-Path (Join-Path $RootDir "backend")

$activateBat1 = Join-Path $BackendDir "venv\Scripts\activate.bat"
$activateBat2 = Join-Path $BackendDir ".venv\Scripts\activate.bat"
$activateBat  = $null
if (Test-Path $activateBat1) { $activateBat = $activateBat1 }
elseif (Test-Path $activateBat2) { $activateBat = $activateBat2 }

if (-not $activateBat) {
  throw "No virtual environment found in backend (.venv or venv missing)"
}

Write-Host "Using virtual environment: $activateBat" -ForegroundColor DarkCyan

Write-Host "`n[1/3] Starting Angular Frontend..." -ForegroundColor Cyan
$frontendCmd = "cd /d `"$FrontendDir`" && npm run start"
$feProc = Start-Process -FilePath "cmd.exe" `
  -ArgumentList "/k", $frontendCmd `
  -PassThru

Write-Host "[2/3] Starting Python Backend (via venv)..." -ForegroundColor Cyan
$backendCmd = "cd /d `"$BackendDir`" && call `"$activateBat`" && python main.py"
$beProc = Start-Process -FilePath "cmd.exe" `
  -ArgumentList "/k", $backendCmd `
  -PassThru

Write-Host "[3/3] Starting Celery Worker (via venv)..." -ForegroundColor Cyan
$celeryCmd = "cd /d `"$BackendDir`" && call `"$activateBat`" && celery -A config.celeryConfig.celery_app worker -l info --pool=solo"
$ceProc = Start-Process -FilePath "cmd.exe" `
  -ArgumentList "/k", $celeryCmd `
  -PassThru

Write-Host "`nAll services launched successfully!"
Write-Host ("  Frontend PID: {0}" -f $feProc.Id)
Write-Host ("  Backend  PID: {0}" -f $beProc.Id)
Write-Host ("  Celery   PID: {0}" -f $ceProc.Id)
Write-Host "`nPress Ctrl+C or close this window to stop everything..." -ForegroundColor Yellow

try {
  while ($true) { Start-Sleep -Seconds 2 }
}
finally {
  Write-Host "`nStopping all services..." -ForegroundColor Yellow
  foreach ($p in @($feProc, $beProc, $ceProc)) {
    try {
      if ($p -and -not $p.HasExited) {
        & taskkill /T /PID $p.Id /F | Out-Null
        Write-Host "Killed PID $($p.Id)" -ForegroundColor DarkYellow
      }
    } catch {
      Write-Host "Note: could not kill PID $($p.Id): $($_.Exception.Message)" -ForegroundColor DarkGray
    }
  }
  Write-Host "`nAll services stopped cleanly. Done." -ForegroundColor Green
}
