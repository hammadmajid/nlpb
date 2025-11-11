#!/bin/bash
# Start FastAPI Backend

echo "🚀 Starting NLP Business Intelligence Backend API..."
cd "$(dirname "$0")"
uv run python backend/main.py
