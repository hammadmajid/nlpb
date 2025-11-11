# Command Reference

Quick reference for common commands used in this project.

## 📦 Setup & Installation

```bash
# Navigate to project
cd ~/Code/nlpb

# Install all dependencies
uv sync

# Install with dev dependencies
uv sync --all-extras

# Update dependencies
uv lock --upgrade

# Download NLTK data (for TextBlob)
uv run python -c "import nltk; nltk.download('brown'); nltk.download('punkt')"
```

## 🚀 Running the Application

### Backend API
```bash
# Using the startup script
./start-backend.sh

# Or manually
uv run python backend/main.py

# Or with uvicorn directly
uv run uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Dashboard
```bash
# Using the startup script
./start-frontend.sh

# Or manually
uv run streamlit run frontend/app.py

# On different port
uv run streamlit run frontend/app.py --server.port 8502
```

## 🧪 Testing

```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run specific test file
uv run pytest tests/backend/test_sentiment.py

# Run with coverage
uv run pytest --cov=backend --cov-report=html
```

## 🔍 Code Quality

```bash
# Format code with black
uv run black backend/ frontend/

# Lint with ruff
uv run ruff check backend/ frontend/

# Auto-fix with ruff
uv run ruff check --fix backend/ frontend/

# Type checking (if mypy installed)
uv run mypy backend/
```

## 📊 API Testing

```bash
# Test health endpoint
curl http://localhost:8000/health

# Test sentiment analysis
curl -X POST http://localhost:8000/api/sentiment/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "This is amazing!"}'

# Test resume screening
curl -X POST http://localhost:8000/api/resume/screen \
  -H "Content-Type: application/json" \
  -d '{"resume_text": "Python developer with 5 years experience", "job_description": "Looking for Python developer"}'

# View API documentation
open http://localhost:8000/docs
```

## 🐛 Debugging

```bash
# Check if ports are in use
lsof -i :8000  # Backend
lsof -i :8501  # Frontend

# Kill process on port
lsof -ti:8000 | xargs kill -9

# Check Python version
uv run python --version

# List installed packages
uv pip list

# Check uv environment
uv venv info
```

## 📝 Development

```bash
# Add new dependency
uv add package-name

# Add dev dependency
uv add --dev package-name

# Remove dependency
uv remove package-name

# Create new migration (if using alembic)
uv run alembic revision --autogenerate -m "message"

# Run Jupyter notebook
uv run jupyter notebook notebooks/
```

## 🔧 Project Management

```bash
# View project structure
tree -L 3 -I '__pycache__|*.pyc|.venv'

# Count lines of code
find . -name "*.py" -not -path "./.venv/*" -exec wc -l {} + | tail -1

# Search for TODO comments
grep -r "TODO" --include="*.py" backend/ frontend/

# Find large files
find . -type f -size +1M -not -path "./.venv/*"
```

## 📦 Data Management

```bash
# Create sample data directory
mkdir -p data/samples

# Clear upload directory
rm -rf data/uploads/*

# Backup data
tar -czf data_backup.tar.gz data/

# Restore data
tar -xzf data_backup.tar.gz
```

## 🚢 Deployment (Future)

```bash
# Build Docker image (when Dockerfile added)
docker build -t nlpb-backend .
docker build -t nlpb-frontend -f Dockerfile.frontend .

# Run with Docker Compose
docker-compose up -d

# Export requirements for deployment
uv pip compile pyproject.toml -o requirements.txt
```

## 🔄 Git Operations

```bash
# Initialize git (if needed)
git init
git add .
git commit -m "Initial commit"

# Create new branch
git checkout -b feature/new-feature

# View changes
git status
git diff

# Commit changes
git add .
git commit -m "Add new feature"

# Push to remote
git push origin main
```

## 📈 Monitoring & Logs

```bash
# View backend logs (if using systemd)
journalctl -u nlpb-backend -f

# View Streamlit logs
tail -f ~/.streamlit/logs/*.log

# Monitor resource usage
htop
```

## 💡 Helpful Aliases

Add these to your `~/.bashrc` or `~/.zshrc`:

```bash
alias nlpb-backend='cd ~/Code/nlpb && ./start-backend.sh'
alias nlpb-frontend='cd ~/Code/nlpb && ./start-frontend.sh'
alias nlpb-test='cd ~/Code/nlpb && uv run pytest -v'
alias nlpb-format='cd ~/Code/nlpb && uv run black backend/ frontend/'
```

## 🆘 Common Issues

### Issue: Port already in use
```bash
# Find and kill process
lsof -ti:8000 | xargs kill -9
```

### Issue: Module not found
```bash
# Reinstall dependencies
uv sync --reinstall
```

### Issue: Permission denied
```bash
# Make scripts executable
chmod +x start-backend.sh start-frontend.sh
```

### Issue: NLTK data not found
```bash
# Download NLTK data
uv run python -c "import nltk; nltk.download('all')"
```

## 📚 Resources

- FastAPI Docs: https://fastapi.tiangolo.com/
- Streamlit Docs: https://docs.streamlit.io/
- TextBlob Docs: https://textblob.readthedocs.io/
- uv Docs: https://github.com/astral-sh/uv

---

**Pro Tip**: Use `uv run` before any Python command to ensure you're using the project's virtual environment!
