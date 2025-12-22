$ErrorActionPreference = "Stop"

function Info($m) { Write-Host "[INFO]  $m" -ForegroundColor Cyan }
function Ok($m)   { Write-Host "[OK]    $m" -ForegroundColor Green }
function Warn($m) { Write-Warning $m }
function Err($m)  { Write-Host "[ERR]   $m" -ForegroundColor Red }

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot  = Join-Path $scriptDir ".."
$frontend  = Join-Path $repoRoot "frontend"
$backend   = Join-Path $repoRoot "backend"

if (-not (Test-Path $frontend)) { throw "Frontend directory not found: $frontend" }
if (-not (Test-Path $backend))  { throw "Backend directory not found: $backend"  }

function Invoke-Cmd {
  param(
    [Parameter(Mandatory)][string]$Command,
    [Parameter(Mandatory)][string]$WorkingDirectory
  )
  Info "cd $WorkingDirectory && $Command"
  $p = Start-Process -FilePath "cmd.exe" -ArgumentList "/c", $Command `
       -WorkingDirectory $WorkingDirectory -NoNewWindow -PassThru -Wait
  if ($p.ExitCode -ne 0) { throw "Command failed with exit code $($p.ExitCode): $Command" }
}

function Ensure-BackendEnv {
  param([string]$BackendDir)
  $envPath    = Join-Path $BackendDir ".env"
  $envExample = Join-Path $BackendDir ".env.example"
  $envSample  = Join-Path $BackendDir ".env.sample"

  if (Test-Path $envPath) {
    Ok "Found backend .env at $envPath"
    return
  }

  if (Test-Path $envExample -or Test-Path $envSample) {
    Write-Host "[ERR] No .env found in backend." -ForegroundColor Red
    Write-Host "      You may copy from .env.example or .env.sample manually," -ForegroundColor Yellow
    Write-Host "      or run: .\bin\setup.ps1" -ForegroundColor Yellow
    exit 1
  }

  Write-Host "[ERR] No .env file found in backend directory: $BackendDir" -ForegroundColor Red
  Write-Host "      Please create one or run: .\bin\setup.ps1" -ForegroundColor Yellow
  exit 1
}

try {
    $nodeVersion = & node --version 2>$null
    if (-not $nodeVersion) { throw "Node.js not found" }
    Write-Host "[OK] Node.js version: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERR] Node.js is not installed or not on PATH." -ForegroundColor Red
    exit 1
}

try {
    $pythonVersion = & python --version 2>$null
    if (-not $pythonVersion) { throw "Python not found" }
    Write-Host "[OK] Python version: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERR] Python is not installed or not on PATH." -ForegroundColor Red
    exit 1
}

Write-Host "`n=== Frontend setup ==="
if (Test-Path (Join-Path $frontend "package.json")) {
  $hasLock = (Test-Path (Join-Path $frontend "package-lock.json")) -or (Test-Path (Join-Path $frontend "npm-shrinkwrap.json"))
  if ($hasLock) {
    try { Invoke-Cmd -Command "npm ci" -WorkingDirectory $frontend; Ok "Frontend dependencies installed (npm ci)." }
    catch { Warn "npm ci failed, falling back to npm install..."; Invoke-Cmd -Command "npm install" -WorkingDirectory $frontend; Ok "Frontend dependencies installed (npm install)." }
  } else {
    Invoke-Cmd -Command "npm install" -WorkingDirectory $frontend
    Ok "Frontend dependencies installed (npm install)."
  }
} else {
  Warn "No package.json found in $frontend. Skipping frontend install."
}

Write-Host "`n=== Backend setup ==="
Ensure-BackendEnv -BackendDir $backend

$venvDir = Join-Path $backend "venv"
$venvPy  = Join-Path $venvDir "Scripts\python.exe"
if (-not (Test-Path $venvPy)) {
  Info "Creating virtual environment at $venvDir ..."
  Invoke-Cmd -Command "python -m venv `"$venvDir`"" -WorkingDirectory $backend
} else {
  Info "Using existing virtual environment: $venvDir"
}
if (-not (Test-Path $venvPy)) { throw "Virtual environment python not found at $venvPy" }

Info "Upgrading pip in venv..."
& $venvPy -m pip install --upgrade pip | Out-Host

$reqTxt  = Join-Path $backend "requirements.txt"
$pyproj  = Join-Path $backend "pyproject.toml"
$setupPy = Join-Path $backend "setup.py"

if (Test-Path $reqTxt) {
  Info "Installing dependencies from requirements.txt ..."
  & $venvPy -m pip install -r $reqTxt | Out-Host
  if ($LASTEXITCODE -ne 0) { throw "pip install -r requirements.txt failed." }
} elseif (Test-Path $pyproj) {
  Info "pyproject.toml found; installing package in editable mode ..."
  & $venvPy -m pip install -e $backend | Out-Host
  if ($LASTEXITCODE -ne 0) { throw "pip install -e (pyproject) failed." }
} elseif (Test-Path $setupPy) {
  Info "setup.py found; installing package ..."
  & $venvPy -m pip install -e $backend | Out-Host
  if ($LASTEXITCODE -ne 0) { throw "pip install -e (setup.py) failed." }
} else {
  Warn "No requirements.txt / pyproject.toml / setup.py found in $backend. Skipping dependency install."
}
Ok "Backend dependencies installed."

Write-Host "`nSetup finished successfully."
