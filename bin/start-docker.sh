#!/usr/bin/env bash
set -euo pipefail

REBUILD=false
COMPOSE_FILE="docker-compose.yml"
DB_SERVICE="db"
BACKEND_SERVICE="backend"
FRONTEND_SERVICE="frontend"
CELERY_SERVICE="celery"
PG_USER="postgres"
PG_DB="postgres"

for arg in "$@"; do
  case $arg in
    --rebuild|-r)
      REBUILD=true
      shift
      ;;
    --file=*)
      COMPOSE_FILE="${arg#*=}"
      shift
      ;;
  esac
done

function step() {
  echo -e "\033[36m==> $1\033[0m"
}

BUILD_CMD=(docker compose -f "$COMPOSE_FILE" build)
if $REBUILD; then BUILD_CMD+=("--no-cache"); fi
step "Building images..."
"${BUILD_CMD[@]}"

step "Starting database and redis..."
docker compose -f "$COMPOSE_FILE" up -d "$DB_SERVICE" redis

step "Waiting for Postgres ($DB_SERVICE) to be ready..."
MAX_ATTEMPTS=60
ATTEMPT=0
until docker compose -f "$COMPOSE_FILE" exec -T "$DB_SERVICE" pg_isready -U "$PG_USER" -d "$PG_DB" >/dev/null 2>&1; do
  ATTEMPT=$((ATTEMPT+1))
  if (( ATTEMPT >= MAX_ATTEMPTS )); then
    echo "❌ Postgres did not become ready in time."
    exit 1
  fi
  sleep 2
done

step "Applying Alembic migrations..."
docker compose -f "$COMPOSE_FILE" run --rm "$BACKEND_SERVICE" alembic upgrade head

step "Starting backend, frontend, and celery (attached)..."
echo ""
echo "   🌐 Frontend: http://localhost:3050"
echo "   🐍 Backend:  http://localhost:8050"
echo "   ⚙️  Celery logs: docker logs -f easyfood-celery"
echo ""
echo "Press Ctrl+C to stop all containers."

docker compose -f "$COMPOSE_FILE" up "$BACKEND_SERVICE" "$FRONTEND_SERVICE" "$CELERY_SERVICE"
