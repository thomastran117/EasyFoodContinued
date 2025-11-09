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
EOF

echo "Created .env at $env_file"
