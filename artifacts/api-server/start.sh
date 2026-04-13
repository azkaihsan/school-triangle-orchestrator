#!/bin/bash
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
if [ "${NODE_ENV:-development}" = "production" ]; then
    exec uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8080}" --workers 2
else
    exec uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8080}" --reload
fi
