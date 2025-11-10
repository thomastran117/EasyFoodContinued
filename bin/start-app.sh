#!/usr/bin/env bash
set -e

if command -v node >/dev/null 2>&1 && command -v npm >/dev/null 2>&1; then
  echo -e "\033[0;32mNode: $(node -v)  npm: $(npm -v)\033[0m"
else
  echo " Node.js (and npm) are not installed or not on PATH."
  exit 1
fi

if command -v python >/dev/null 2>&1; then
  echo -e "\033[0;32mPython: $(python --version 2>&1)\033[0m"
else
  echo "Python is not installed or not on PATH."
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
FRONTEND_DIR="$ROOT_DIR/frontend"
BACKEND_DIR="$ROOT_DIR/backend"

if [ -f "$BACKEND_DIR/venv/bin/activate" ]; then
  ACTIVATE="$BACKEND_DIR/venv/bin/activate"
elif [ -f "$BACKEND_DIR/.venv/bin/activate" ]; then
  ACTIVATE="$BACKEND_DIR/.venv/bin/activate"
else
  echo "No virtual environment found in backend (.venv or venv missing)"
  exit 1
fi

echo -e "\033[0;36mUsing virtual environment: $ACTIVATE\033[0m"

echo -e "\n\033[0;36m[1/3] Starting Angular Frontend...\033[0m"
cd "$FRONTEND_DIR"
npm run start &
FE_PID=$!

echo -e "\033[0;36m[2/3] Starting Python Backend (via venv)...\033[0m"
cd "$BACKEND_DIR"
bash -c "source '$ACTIVATE' && python main.py" &
BE_PID=$!

echo -e "\033[0;36m[3/3] Starting Celery Worker (via venv)...\033[0m"
bash -c "source '$ACTIVATE' && celery -A config.celeryConfig.celery_app worker -l info --pool=solo" &
CE_PID=$!

echo -e "\n✅ All services launched successfully!"
echo "  Frontend PID: $FE_PID"
echo "  Backend  PID: $BE_PID"
echo "  Celery   PID: $CE_PID"
echo -e "\nPress Ctrl+C to stop everything..."
echo

trap cleanup INT

cleanup() {
  echo -e "\n\033[1;33mStopping all services...\033[0m"
  for pid in $FE_PID $BE_PID $CE_PID; do
    if kill -0 $pid 2>/dev/null; then
      kill -TERM "$pid" 2>/dev/null || true
      echo "Killed PID $pid"
    fi
  done
  echo -e "\n\033[0;32mAll services stopped cleanly. Done.\033[0m"
  exit 0
}

while true; do sleep 2; done
