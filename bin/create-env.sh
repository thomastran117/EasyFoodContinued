set -euo pipefail

FORCE=false
RANDOM_SECRET=false

for arg in "$@"; do
  case "$arg" in
    --force) FORCE=true ;;
    --random-secret) RANDOM_SECRET=true ;;
  esac
done

backend_dir="backend"
env_file="$backend_dir/.env"

if [ ! -d "$backend_dir" ]; then
  mkdir -p "$backend_dir"
  echo "Created backend directory."
fi

if [ -f "$env_file" ] && [ "$FORCE" = false ]; then
  echo "Warning: $env_file already exists. Use --force to overwrite."
  exit 0
fi

if [ "$RANDOM_SECRET" = true ]; then
  secret=$(openssl rand -base64 32)
else
  secret="change_me_dev_secret"
fi

cat > "$env_file" <<EOF
PORT=8090

##############################################
# Database & Redis
##############################################
# Default local Postgres connection (user: postgres, pass: postgres, db: postgres)
# If running inside Docker and your app connects to the compose service, use host 'db' instead of 'localhost':
#   DATABASE_URL="postgresql+psycopg://postgres:postgres@db:5432/postgres"
DATABASE_URL="postgresql+psycopg://postgres:postgres@localhost:5432/postgres"

# Default local Redis connection (DB 0). For Docker compose service, host is 'redis':
#   REDIS_URL="redis://redis:6379/0"
REDIS_URL="redis://localhost:6379/0"

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
GOOGLE_REDIRECT_URI="http://localhost:8090/api/auth/google/callback"

##############################################
# Microsoft OAuth2
##############################################
MS_TENANT_ID="your-microsoft-tenant-id"
MS_CLIENT_ID="your-microsoft-client-id"
MS_CLIENT_SECRET="your-microsoft-client-secret"
MS_REDIRECT_URI="http://localhost:8090/api/auth/microsoft/callback"
EOF

echo "Created .env at $env_file"
