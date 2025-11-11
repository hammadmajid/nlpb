#!/bin/bash
# Start Streamlit Frontend

echo "🚀 Starting NLP Business Intelligence Dashboard..."
cd "$(dirname "$0")"
uv run streamlit run frontend/app.py
