#!/bin/bash

set -euo pipefail

info() { printf '[INFO]  %s\n' "$*"; }
ok()   { printf '[OK]    %s\n' "$*"; }
warn() { printf '[WARN]  %s\n' "$*" >&2; }
err()  { printf '[ERR]   %s\n' "$*" >&2; }

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "$SCRIPT_DIR/.." && pwd)"
FRONTEND="$REPO_ROOT/frontend"
BACKEND="$REPO_ROOT/backend"

[[ -d "$FRONTEND" ]] || { err "Frontend directory not found: $FRONTEND"; exit 1; }
[[ -d "$BACKEND"  ]] || { err "Backend directory not found: $BACKEND"; exit 1; }

if ! command -v node >/dev/null 2>&1; then
  err "Node.js is not installed or not on PATH."
  exit 1
fi
ok "Node.js version: $(node --version)"

PYTHON_BIN="python3"
command -v "$PYTHON_BIN" >/dev/null 2>&1 || PYTHON_BIN="python"
if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  err "Python is not installed or not on PATH."
  exit 1
fi
ok "Python version: $($PYTHON_BIN --version 2>&1)"

ensure_backend_env() {
  local backend_dir="$1"
  local env_path="$backend_dir/.env"
  local env_example="$backend_dir/.env.example"
  local env_sample="$backend_dir/.env.sample"

  if [[ -f "$env_path" ]]; then
    ok "Found backend .env at $env_path"
    return
  fi

  if [[ -f "$env_example" || -f "$env_sample" ]]; then
    err "No .env found in backend."
    warn "You may copy from .env.example or .env.sample manually,"
    warn "or run: ./bin/create-env.sh"
    exit 1
  fi

  err "No .env file found in backend directory: $backend_dir"
  warn "Please create one or run: ./bin/create-env.sh"
  exit 1
}

echo
echo "=== Frontend setup ==="
if [[ -f "$FRONTEND/package.json" ]]; then
  pushd "$FRONTEND" >/dev/null
  if [[ -f package-lock.json || -f npm-shrinkwrap.json ]]; then
    if npm ci; then
      ok "Frontend dependencies installed (npm ci)."
    else
      warn "npm ci failed, falling back to npm install..."
      npm install
      ok "Frontend dependencies installed (npm install)."
    fi
  else
    npm install
    ok "Frontend dependencies installed (npm install)."
  fi
  popd >/dev/null
else
  warn "No package.json found in $FRONTEND. Skipping frontend install."
fi

echo
echo "=== Backend setup ==="
ensure_backend_env "$BACKEND"

VENV_DIR="$BACKEND/venv"
VENV_PY="$VENV_DIR/bin/python"

if [[ ! -x "$VENV_PY" ]]; then
  info "Creating virtual environment at $VENV_DIR ..."
  "$PYTHON_BIN" -m venv "$VENV_DIR"
else
  info "Using existing virtual environment: $VENV_DIR"
fi

info "Upgrading pip in venv..."
"$VENV_PY" -m pip install --upgrade pip

REQ_TXT="$BACKEND/requirements_linux.txt"
REQ_DEV="$BACKEND/requirements_linux-dev.txt"
PYPROJ="$BACKEND/pyproject.toml"
SETUP_PY="$BACKEND/setup.py"

if [[ -f "$REQ_TXT" ]]; then
  info "Installing dependencies from requirements_linux.txt ..."
  "$VENV_PY" -m pip install -r "$REQ_TXT"
  if [[ -f "$REQ_DEV" ]]; then
    info "Installing dev dependencies from requirements_linux-dev.txt ..."
    "$VENV_PY" -m pip install -r "$REQ_DEV"
  fi
elif [[ -f "$PYPROJ" ]]; then
  info "pyproject.toml found; installing package in editable mode ..."
  "$VENV_PY" -m pip install -e "$BACKEND"
elif [[ -f "$SETUP_PY" ]]; then
  info "setup.py found; installing package ..."
  "$VENV_PY" -m pip install -e "$BACKEND"
else
  warn "No requirements_linux.txt / pyproject.toml / setup.py found in $BACKEND. Skipping dependency install."
fi
ok "Backend dependencies installed."

echo
echo "=== Alembic migration ==="
if [[ ! -f "$BACKEND/alembic.ini" ]]; then
  warn "alembic.ini not found in $BACKEND. Skipping migrations."
else
  pushd "$BACKEND" >/dev/null
  info "Running 'alembic upgrade head' with venv python..."
  if ! "$VENV_PY" -m alembic upgrade head; then
    err "alembic upgrade head failed. Ensure Alembic is in your requirements and DATABASE_URL is valid."
    popd >/dev/null
    exit 1
  fi
  popd >/dev/null
  ok "Alembic migration completed."
fi

echo
echo "Setup finished successfully."
