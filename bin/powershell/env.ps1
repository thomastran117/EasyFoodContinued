param (
    [switch]$Force
)

# ------------------------------------------------------------
# Resolve script root safely (works even when dot-sourced)
# ------------------------------------------------------------
$ScriptRoot =
    if ($PSScriptRoot) {
        $PSScriptRoot
    } else {
        Split-Path -Parent $MyInvocation.MyCommand.Definition
    }

$ProjectRoot = Resolve-Path (Join-Path $ScriptRoot "..\..\")
$BackendPath = Join-Path $ProjectRoot "backend"
$FrontendPath = Join-Path $ProjectRoot "frontend"

$EnvFilePathBackend  = Join-Path $BackendPath  ".env"
$EnvFilePathFrontend = Join-Path $FrontendPath ".env"

# ------------------------------------------------------------
# Validate folders
# ------------------------------------------------------------
if (-not (Test-Path $BackendPath)) {
    Write-Error "Backend folder not found at: $BackendPath"
    exit 1
}

if (-not (Test-Path $FrontendPath)) {
    Write-Error "Frontend folder not found at: $FrontendPath"
    exit 1
}

# ------------------------------------------------------------
# Prevent overwrite unless -Force
# ------------------------------------------------------------
if (-not $Force) {
    if (Test-Path $EnvFilePathBackend) {
        Write-Error "Backend .env already exists. Use -Force to overwrite."
        exit 1
    }
    if (Test-Path $EnvFilePathFrontend) {
        Write-Error "Frontend .env already exists. Use -Force to overwrite."
        exit 1
    }
}

# ------------------------------------------------------------
# Frontend .env
# ------------------------------------------------------------
$envContent_frontend = @'
##############################################
# Server
##############################################

BACKEND_URL="http://localhost:8040/api"
FRONTEND_URL="http://localhost:3040"
GOOGLE_CLIENT_ID="google-client"
MSAL_CLIENT_ID="msal-client"
GOOGLE_SITE_KEY="google-site"
PAYPAL_MODE="sandbox"
PAYPAL_CLIENT_ID="id"
PAYPAL_SECRET_KEY="secret"
'@

$envContent_backend = @'
##############################################
# Configuration
##############################################

ENVIRONMENT="development"

##############################################
# Server
##############################################

FRONTEND_CLIENT="http://localhost:3040"
PORT=8040

##############################################
# Databases
##############################################

REDIS_URL="redis://127.0.0.1:6379"
MONGO_URL="mongodb://localhost:27017/app"
RABBITMQ_URL="amqp://guest:guest@localhost:5672"

##############################################
# Workers
##############################################

CELERY_BROKER_URL="redis://127.0.0.1:6379/0"
CELERY_RESULT_BACKEND="redis://127.0.0.1:6379/1"

##############################################
# Security
##############################################

SECRET_KEY="access-jwt-token"
ALGORITHM="HS256"
GOOGLE_SECRET_KEY=""

##############################################
# CORS Configuration
##############################################

CORS_ALLOWED_REGION=["http://localhost:3040"]

##############################################
# Email (SMTP credentials)
##############################################

EMAIL_USER=""
EMAIL_PASS=""

##############################################
# OAuth
##############################################

GOOGLE_CLIENT_ID=""
MS_TENANT_ID="common"
MS_CLIENT_ID=""

##############################################
# Paypal
##############################################

PAYPAL_MODE="sandbox"
PAYPAL_CLIENT_ID=""
PAYPAL_SECRET_KEY=""
'@

# ------------------------------------------------------------
# Write files (UTF-8 safe for Windows + Node)
# ------------------------------------------------------------
Set-Content -Path $EnvFilePathBackend  -Value $envContent_backend  -Encoding UTF8
Write-Host "Backend .env created at: $EnvFilePathBackend"

Set-Content -Path $EnvFilePathFrontend -Value $envContent_frontend -Encoding UTF8
Write-Host "Frontend .env created at: $EnvFilePathFrontend"
