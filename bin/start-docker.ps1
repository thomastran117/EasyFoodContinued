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

Invoke-Step "Starting application stack..."
Write-Host ""
Write-Host "Press Ctrl+C to stop containers." -ForegroundColor Yellow
Write-Host ""
Write-Host "   🌐 Frontend: http://localhost:3040"
Write-Host "   🐍 Backend:  http://localhost:8040"
Write-Host "   ⚙️  Celery Worker: docker logs -f easyfood-celery"
Write-Host ""

docker compose -f $ComposeFile up $BackendService $FrontendService $CeleryService
