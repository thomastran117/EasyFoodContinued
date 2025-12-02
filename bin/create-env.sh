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
EOF

echo "Created .env at $env_file"
