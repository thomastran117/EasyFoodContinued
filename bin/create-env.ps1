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
PORT=8090

##############################################
# Databases
##############################################

DATABASE_URL="postgresql+psycopg://postgres:postgres@localhost:5432/postgres"
REDIS_URL="redis://localhost:6379/0"
MONGO_URL="mongodb://localhost:27017/app"

##############################################
# CORS Configuration
##############################################
# Allowed origins for cross-origin requests (JSON array as string)
# Typical dev front-end address:
#   ["http://localhost:3090"]
CORS_ALLOWED_REGION=["http://localhost:3090"]

##############################################
# Security / JWT
##############################################
# Secret key for signing tokens (use a strong random value in production)
SECRET_KEY="$secret"
# JWT signing algorithm
ALGORITHM="HS256"
# Token expiration in minutes
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
GOOGLE_CLIENT_SECRET="your-google-client-secret"
GOOGLE_REDIRECT_URI="http://localhost:8040/api/auth/google/callback"

##############################################
# Microsoft OAuth2
##############################################
MS_TENANT_ID="your-microsoft-tenant-id"
MS_CLIENT_ID="your-microsoft-client-id"
MS_CLIENT_SECRET="your-microsoft-client-secret"
MS_REDIRECT_URI="http://localhost:8040/api/auth/microsoft/callback"
"@

$envContent | Set-Content -Path $envPath -Encoding UTF8 -NoNewline
Write-Host "Created .env at $envPath"
