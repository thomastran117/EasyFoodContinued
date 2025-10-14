#!/bin/bash

set -euo pipefail

REBUILD=false
COMPOSE_FILE="docker-compose.yml"
DB_SERVICE="db"
BACKEND_SERVICE="backend"
FRONTEND_SERVICE="frontend"
PG_USER="postgres"
PG_DB="postgres"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --rebuild) REBUILD=true; shift ;;
    --file) COMPOSE_FILE="$2"; shift 2 ;;
    --db) DB_SERVICE="$2"; shift 2 ;;
    --backend) BACKEND_SERVICE="$2"; shift 2 ;;
    --frontend) FRONTEND_SERVICE="$2"; shift 2 ;;
    --pg-user) PG_USER="$2"; shift 2 ;;
    --pg-db) PG_DB="$2"; shift 2 ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

if docker compose version >/dev/null 2>&1; then
  COMPOSE=("docker" "compose" "-f" "$COMPOSE_FILE")
elif command -v docker-compose >/dev/null 2>&1; then
  COMPOSE=("docker-compose" "-f" "$COMPOSE_FILE")
else
  echo "Error: neither 'docker compose' nor 'docker-compose' found on PATH." >&2
  exit 1
fi

step() { printf '\n==> %s\n' "$*"; }

BUILD_CMD=("${COMPOSE[@]}" build)
$REBUILD && BUILD_CMD+=("--no-cache")
step "Building images..."
"${BUILD_CMD[@]}"

step "Starting database and redis..."
"${COMPOSE[@]}" up -d "$DB_SERVICE" redis

step "Waiting for Postgres ($DB_SERVICE) to be ready..."
max_attempts=60
attempt=0
until "${COMPOSE[@]}" exec -T "$DB_SERVICE" pg_isready -U "$PG_USER" -d "$PG_DB" >/dev/null 2>&1; do
  attempt=$((attempt+1))
  if (( attempt >= max_attempts )); then
    echo "Postgres did not become ready in time." >&2
    exit 1
  fi
  sleep 2
done

step "Applying Alembic migrations (alembic upgrade head)..."
"${COMPOSE[@]}" run --rm "$BACKEND_SERVICE" alembic upgrade head

step "Starting backend and frontend (attached)..."
echo "Press Ctrl+C to stop containers."
echo
echo "   Frontend: http://localhost:3050"
echo "   Backend:  http://localhost:8050/"
echo

exec "${COMPOSE[@]}" up "$BACKEND_SERVICE" "$FRONTEND_SERVICE"
