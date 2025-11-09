#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REPO_ROOT="$(realpath "$SCRIPT_DIR/..")"
FRONTEND="$REPO_ROOT/frontend"
BACKEND="$REPO_ROOT/backend"

VENV_ACTIVATE=""
if [[ -f "$BACKEND/venv/bin/activate" ]]; then
  VENV_ACTIVATE="$BACKEND/venv/bin/activate"
elif [[ -f "$BACKEND/.venv/bin/activate" ]]; then
  VENV_ACTIVATE="$BACKEND/.venv/bin/activate"
fi

echo -e "\033[36m[1/3] Starting frontend...\033[0m"
(cd "$FRONTEND" && npm run start -- --host 0.0.0.0 --port 3050) &
FRONTEND_PID=$!

echo -e "\033[36m[2/3] Starting backend...\033[0m"
if [[ -n "$VENV_ACTIVATE" ]]; then
  echo -e "🐍 Using virtualenv: $VENV_ACTIVATE"
  bash -c "source '$VENV_ACTIVATE' && cd '$BACKEND' && python main.py" &
else
  echo -e "⚠️ No venv found, using system Python"
  (cd "$BACKEND" && python main.py) &
fi
BACKEND_PID=$!

echo -e "\033[36m[3/3] Starting Celery worker...\033[0m"
if [[ -n "$VENV_ACTIVATE" ]]; then
  bash -c "source '$VENV_ACTIVATE' && cd '$BACKEND' && celery -A config.celeryConfig.celery_app worker -l info --pool=solo" &
else
  (cd "$BACKEND" && celery -A config.celeryConfig.celery_app worker -l info --pool=solo) &
fi
CELERY_PID=$!

echo ""
echo -e "\033[32m✅ All services running:\033[0m"
echo "   Frontend: http://localhost:3050"
echo "   Backend:  http://localhost:8050"
echo "   Celery worker active"
echo ""
echo "Press Ctrl+C to stop all processes."

trap 'echo -e "\n🛑 Stopping services..."; kill $FRONTEND_PID $BACKEND_PID $CELERY_PID 2>/dev/null; wait; echo "✅ All stopped."; exit 0' SIGINT SIGTERM

wait
