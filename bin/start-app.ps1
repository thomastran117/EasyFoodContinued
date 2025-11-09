$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot  = Join-Path $scriptDir ".."
$frontend  = Join-Path $repoRoot "frontend"
$backend   = Join-Path $repoRoot "backend"

Write-Host "===============================================" -ForegroundColor DarkGray
Write-Host "🚀 Starting EasyFood Services (frontend + backend + celery)" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor DarkGray

Write-Host "`n[1/3] Starting Frontend..." -ForegroundColor Cyan
$frontendProc = Start-Process `
  -FilePath "cmd.exe" `
  -ArgumentList "/c","npm run start" `
  -WorkingDirectory $frontend `
  -NoNewWindow `
  -PassThru

$activateBat1 = Join-Path $backend "venv\Scripts\activate.bat"
$activateBat2 = Join-Path $backend ".venv\Scripts\activate.bat"
$activateBat  = $null
if (Test-Path $activateBat1) { $activateBat = $activateBat1 }
elseif (Test-Path $activateBat2) { $activateBat = $activateBat2 }

if ($activateBat) {
  $backendCmd = "call `"$activateBat`" && python main.py"
  Write-Host "[2/3] 🐍 Using virtual environment: $activateBat" -ForegroundColor DarkCyan
} else {
  $backendCmd = "python main.py"
  Write-Host "[2/3] ⚠️ No venv found in backend. Using system Python." -ForegroundColor Yellow
}

Write-Host "[2/3] Starting Backend..." -ForegroundColor Cyan
$backendProc = Start-Process `
  -FilePath "cmd.exe" `
  -ArgumentList "/c",$backendCmd `
  -WorkingDirectory $backend `
  -NoNewWindow `
  -PassThru

Write-Host "[3/3] Starting Celery Worker..." -ForegroundColor Cyan

$celeryCmd = if ($activateBat) {
  "call `"$activateBat`" && celery -A config.celeryConfig.celery_app worker -l info --pool=solo"
} else {
  "celery -A config.celeryConfig.celery_app worker -l info --pool=solo"
}

$celeryProc = Start-Process `
  -FilePath "cmd.exe" `
  -ArgumentList "/c", $celeryCmd `
  -WorkingDirectory $backend `
  -NoNewWindow `
  -PassThru

Write-Host "`n✅ All services started successfully!"
Write-Host "   • Frontend running..."
Write-Host "   • Backend running..."
Write-Host "   • Celery worker running..."
Write-Host "`nPress Ctrl+C to stop all services." -ForegroundColor Green

try {
  Wait-Process -Id $frontendProc.Id,$backendProc.Id,$celeryProc.Id
}
finally {
  Write-Host "`n⚠️ Stopping all services..." -ForegroundColor Yellow

  if ($frontendProc -and -not $frontendProc.HasExited) {
    Stop-Process -Id $frontendProc.Id -Force
    Write-Host "🛑 Frontend stopped."
  }
  if ($backendProc -and -not $backendProc.HasExited) {
    Stop-Process -Id $backendProc.Id -Force
    Write-Host "🛑 Backend stopped."
  }
  if ($celeryProc -and -not $celeryProc.HasExited) {
    Stop-Process -Id $celeryProc.Id -Force
    Write-Host "🛑 Celery worker stopped."
  }

  Write-Host "`n✅ All processes terminated cleanly." -ForegroundColor Green
}
