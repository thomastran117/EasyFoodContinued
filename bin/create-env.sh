#!/bin/bash

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
GOOGLE_REDIRECT_URI="http://localhost:8050/api/auth/google/callback"

##############################################
# Microsoft OAuth2
##############################################
MS_TENANT_ID="your-microsoft-tenant-id"
MS_CLIENT_ID="your-microsoft-client-id"
MS_CLIENT_SECRET="your-microsoft-client-secret"
MS_REDIRECT_URI="http://localhost:8050/api/auth/microsoft/callback"
EOF

echo "Created .env at $env_file"
