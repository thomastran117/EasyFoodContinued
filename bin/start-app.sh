#!/usr/bin/env bash
set -e
trap cleanup SIGINT SIGTERM

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(realpath "${SCRIPT_DIR}/..")"
FRONTEND="${REPO_ROOT}/frontend"
BACKEND="${REPO_ROOT}/backend"

cleanup() {
  echo ""
  echo "⚠️  Stopping all services..."
  [[ -n "$FRONTEND_PID" ]] && kill "$FRONTEND_PID" 2>/dev/null && echo "🛑 Frontend stopped."
  [[ -n "$BACKEND_PID" ]] && kill "$BACKEND_PID" 2>/dev/null && echo "🛑 Backend stopped."
  [[ -n "$CELERY_PID"  ]] && kill "$CELERY_PID"  2>/dev/null && echo "🛑 Celery worker stopped."
  echo "✅ All processes terminated cleanly."
  exit 0
}

echo "==============================================="
echo "🚀 Starting EasyFood Services (frontend + backend + celery)"
echo "==============================================="

echo -e "\n[1/3] Starting Frontend..."
(
  cd "$FRONTEND"
  npm run start &
)
FRONTEND_PID=$!
echo "✅ Frontend started (PID: $FRONTEND_PID)"

ACTIVATE1="${BACKEND}/venv/bin/activate"
ACTIVATE2="${BACKEND}/.venv/bin/activate"

if [[ -f "$ACTIVATE1" ]]; then
  ACTIVATE="$ACTIVATE1"
elif [[ -f "$ACTIVATE2" ]]; then
  ACTIVATE="$ACTIVATE2"
fi

if [[ -n "$ACTIVATE" ]]; then
  echo -e "\n[2/3] 🐍 Using virtual environment: $ACTIVATE"
  (
    cd "$BACKEND"
    source "$ACTIVATE"
    python main.py &
  )
else
  echo -e "\n[2/3] ⚠️ No venv found in backend. Using system Python."
  (
    cd "$BACKEND"
    python main.py &
  )
fi

BACKEND_PID=$!
echo "✅ Backend started (PID: $BACKEND_PID)"

BACKEND_URL="http://127.0.0.1:8050/health"
MAX_RETRIES=30
WAIT_SECONDS=2
echo -e "\n[⏳] Waiting for backend to be ready on $BACKEND_URL..."

for ((i=1; i<=MAX_RETRIES; i++)); do
  if curl -s -o /dev/null -w "%{http_code}" "$BACKEND_URL" | grep -q "200"; then
    echo "✅ Backend is ready after $((i * WAIT_SECONDS))s"
    break
  fi
  sleep "$WAIT_SECONDS"
  if [[ $i -eq $MAX_RETRIES ]]; then
    echo "❌ Backend not ready after $((MAX_RETRIES * WAIT_SECONDS))s. Starting Celery anyway."
  fi
done

echo -e "\n[3/3] Starting Celery Worker..."
if [[ -n "$ACTIVATE" ]]; then
  (
    cd "$BACKEND"
    source "$ACTIVATE"
    celery -A config.celeryConfig.celery_app worker -l info --pool=solo &
  )
else
  (
    cd "$BACKEND"
    celery -A config.celeryConfig.celery_app worker -l info --pool=solo &
  )
fi

CELERY_PID=$!
echo "✅ Celery worker started (PID: $CELERY_PID)"

echo ""
echo "✅ All services started successfully!"
echo "   • Frontend running (PID: $FRONTEND_PID)"
echo "   • Backend running  (PID: $BACKEND_PID)"
echo "   • Celery worker    (PID: $CELERY_PID)"
echo ""
echo "Press Ctrl+C to stop all services."

wait
