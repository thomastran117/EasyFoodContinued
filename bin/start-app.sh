#!/bin/bash

set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "$SCRIPT_DIR/.." && pwd)"
FRONTEND="$REPO_ROOT/frontend"
BACKEND="$REPO_ROOT/backend"

echo "🚀 Starting frontend..."
(
  cd "$FRONTEND"
  npm run start
) &
FRONTEND_PID=$!

VENV_ACTIVATE1="$BACKEND/venv/bin/activate"
VENV_ACTIVATE2="$BACKEND/.venv/bin/activate"
BACKEND_CMD="python main.py"

if [[ -f "$VENV_ACTIVATE1" ]]; then
  BACKEND_CMD="source \"$VENV_ACTIVATE1\" && python main.py"
  echo "🐍 Using virtual environment: $VENV_ACTIVATE1"
elif [[ -f "$VENV_ACTIVATE2" ]]; then
  BACKEND_CMD="source \"$VENV_ACTIVATE2\" && python main.py"
  echo "🐍 Using virtual environment: $VENV_ACTIVATE2"
else
  echo "⚠️ No venv found in backend. Using system Python."
fi

echo "🚀 Starting backend..."
(
  cd "$BACKEND"
  bash -c "$BACKEND_CMD"
) &
BACKEND_PID=$!

echo
echo "Both servers are running. Press Ctrl+C to stop them."

trap 'echo; echo "Stopping servers..."; kill $FRONTEND_PID $BACKEND_PID 2>/dev/null || true; wait $FRONTEND_PID $BACKEND_PID 2>/dev/null || true; echo "✅ All stopped."; exit 0' INT

wait $FRONTEND_PID $BACKEND_PID
