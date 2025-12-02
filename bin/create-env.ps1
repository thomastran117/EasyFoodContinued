param(
    [switch]$Force,
    [switch]$RandomSecret
)

function New-RandomSecret {
    $bytes = New-Object byte[] 32
    [System.Security.Cryptography.RandomNumberGenerator]::Fill($bytes)
    return [Convert]::ToBase64String($bytes)
}

$backendDir = "backend"
if (-not (Test-Path -Path $backendDir -PathType Container)) {
    New-Item -ItemType Directory -Path $backendDir | Out-Null
    Write-Host "Created backend directory."
}

$envPath = Join-Path -Path $backendDir -ChildPath ".env"

if ((Test-Path $envPath) -and -not $Force) {
    Write-Host "Warning: $envPath already exists. Use -Force to overwrite."
    exit 0
}

$secret = if ($RandomSecret) { New-RandomSecret } else { "change_me_dev_secret" }

$envContent = @"
##############################################
# Server
##############################################

FRONTEND_CLIENT="http://localhost:3040"
PORT=8040

##############################################
# Databases
##############################################

DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/easyfoodapp"
REDIS_URL="redis://localhost:6379/0"
MONGO_URL="mongodb://localhost:27017/easyfoodapp"

##############################################
# Workers
##############################################

CELERY_BROKER_URL="redis://127.0.0.1:6379/0"
CELERY_RESULT_BACKEND="redis://127.0.0.1:6379/1"

##############################################
# CORS Configuration
##############################################
CORS_ALLOWED_REGION=["http://localhost:3040"]

##############################################
# Security / JWT
##############################################
SECRET_KEY="super_secret_key"
ALGORITHM="HS256"

##############################################
# Email (SMTP credentials)
##############################################
EMAIL=""
PASSWORD=""

##############################################
# Google OAuth2
##############################################
GOOGLE_CLIENT_ID=""
GOOGLE_SECRET_KEY=""

##############################################
# Microsoft OAuth2
##############################################
MS_TENANT_ID="common"
MS_CLIENT_ID=""

##############################################
# Paypal
##############################################
PAYPAL_MODE="sandbox"
PAYPAL_CLIENT_ID=""
PAYPAL_SECRET_KEY=""
"@

$envContent | Set-Content -Path $envPath -Encoding UTF8 -NoNewline
Write-Host "Created .env at $envPath"
