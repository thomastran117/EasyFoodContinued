$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot  = Join-Path $scriptDir ".."
$frontend  = Join-Path $repoRoot "frontend"
$backend   = Join-Path $repoRoot "backend"

Write-Host "🚀 Starting frontend..." -ForegroundColor Cyan
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
  Write-Host "🐍 Using virtual environment: $activateBat" -ForegroundColor DarkCyan
} else {
  $backendCmd = "python main.py"
  Write-Host "⚠️ No venv found in backend. Using system Python." -ForegroundColor Yellow
}

Write-Host "🚀 Starting backend..." -ForegroundColor Cyan
$backendProc = Start-Process `
  -FilePath "cmd.exe" `
  -ArgumentList "/c",$backendCmd `
  -WorkingDirectory $backend `
  -NoNewWindow `
  -PassThru

Write-Host "`n Both servers are running. Press Ctrl+C to stop them." -ForegroundColor Green

try {
  Wait-Process -Id $frontendProc.Id,$backendProc.Id
} finally {
  Write-Host "`n Stopping servers..." -ForegroundColor Yellow
  if ($frontendProc -and -not $frontendProc.HasExited) { Stop-Process -Id $frontendProc.Id -Force }
  if ($backendProc  -and -not $backendProc.HasExited)  { Stop-Process -Id $backendProc.Id  -Force }
  Write-Host " All stopped." -ForegroundColor Green
}
