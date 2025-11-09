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

FRONTEND_CLIENT="http://localhost:3090"
PORT=8050

##############################################
# Databases
##############################################

DATABASE_URL="postgresql+psycopg://postgres:postgres@localhost:5432/postgres"
REDIS_URL="redis://localhost:6379/0"
MONGO_URL="mongodb://localhost:27017/app"
CELERY_BROKER_URL="redis://127.0.0.1:6379/0"
CELERY_RESULT_BACKEND="redis://127.0.0.1:6379/1"

##############################################
# CORS Configuration
##############################################
CORS_ALLOWED_REGION=["http://localhost:3050"]

##############################################
# Security / JWT
##############################################
SECRET_KEY="$secret"
ALGORITHM="HS256"
EXPIRE_MINUTES="30"

##############################################
# Email (SMTP credentials)
##############################################
EMAIL="example@email.com"
PASSWORD="your_email_password_here"

##############################################
# Google OAuth2
##############################################
GOOGLE_CLIENT_ID="your-google-client-id.apps.googleusercontent.com"
GOOGLE_SECRET_KEY="your-google-client-secret"

##############################################
# Microsoft OAuth2
##############################################
MS_TENANT_ID="your-microsoft-tenant-id"
MS_CLIENT_ID="your-microsoft-client-id"

##############################################
# Paypal
##############################################
PAYPAL_MODE="sandbox"
PAYPAL_CLIENT_ID="paypal_client_id"
PAYPAL_SECRET_KEY="paypal_secret_key"
"@

$envContent | Set-Content -Path $envPath -Encoding UTF8 -NoNewline
Write-Host "Created .env at $envPath"
