param(
  [switch]$Rebuild,
  [string]$ComposeFile = "docker-compose.yml",
  [string]$DbService = "db",
  [string]$BackendService = "backend",
  [string]$FrontendService = "frontend",
  [string]$CeleryService = "celery",
  [string]$PgUser = "postgres",
  [string]$PgDb   = "postgres"
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

function Invoke-Step($msg) {
  Write-Host "==> $msg" -ForegroundColor Cyan
}

$buildArgs = @("compose","-f",$ComposeFile,"build")
if ($Rebuild) { $buildArgs += "--no-cache" }

Invoke-Step "Building Docker images..."
docker @buildArgs

Invoke-Step "Starting Postgres and Redis..."
docker compose -f $ComposeFile up -d $DbService redis

Invoke-Step "Waiting for Postgres ($DbService) to be ready..."
$maxAttempts = 60
$attempt = 0
$pgReady = $false

while (-not $pgReady -and $attempt -lt $maxAttempts) {
  $attempt++
  try {
    docker compose -f $ComposeFile exec -T $DbService pg_isready -U $PgUser -d $PgDb | Out-Null
    $pgReady = $true
  }
  catch {
    Start-Sleep -Seconds 2
  }
}
if (-not $pgReady) { throw "❌ Postgres did not become ready in time." }

Invoke-Step "Applying Alembic migrations..."
docker compose -f $ComposeFile run --rm $BackendService alembic upgrade head

Invoke-Step "Starting application stack..."
Write-Host ""
Write-Host "Press Ctrl+C to stop containers." -ForegroundColor Yellow
Write-Host ""
Write-Host "   🌐 Frontend: http://localhost:3040"
Write-Host "   🐍 Backend:  http://localhost:8040"
Write-Host "   ⚙️  Celery Worker: docker logs -f easyfood-celery"
Write-Host ""

docker compose -f $ComposeFile up $BackendService $FrontendService $CeleryService
