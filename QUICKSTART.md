# Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies
```bash
cd ~/Code/nlpb
uv sync
```

Wait for dependencies to install (may take 2-5 minutes first time).

### Step 2: Start Backend API
Open a terminal and run:
```bash
cd ~/Code/nlpb
./start-backend.sh
```

Or manually:
```bash
uv run python backend/main.py
```

✅ Backend ready when you see: "Uvicorn running on http://0.0.0.0:8000"

### Step 3: Start Frontend Dashboard
Open a **NEW** terminal and run:
```bash
cd ~/Code/nlpb
./start-frontend.sh
```

Or manually:
```bash
uv run streamlit run frontend/app.py
```

✅ Dashboard will auto-open at http://localhost:8501

## 🎯 Try It Out!

### Test Sentiment Analysis
1. Go to "Sentiment Analysis" page
2. Click "Use sample data" checkbox
3. Click "Analyze All"
4. View results and statistics!

### Test Resume Screening
1. Go to "Resume Screening" page
2. Go to "Batch Ranking" tab
3. Click "Use sample resumes" checkbox
4. Click "Rank All Resumes"
5. See ranked results!

### Test Fake News Detection
1. Go to "Fake News Detection" page
2. Click "News Article" button for legitimate content
3. OR click "Clickbait" to see fake news detection
4. View detailed analysis!

## 📚 Next Steps

- Read full [README.md](README.md) for detailed documentation
- Explore API docs at http://localhost:8000/docs
- Check [data/samples/](data/samples/) for example datasets
- Modify services in [backend/services/](backend/services/) for custom logic

## ⚠️ Troubleshooting

**"Module not found" error?**
→ Run `uv sync` again

**"Port already in use"?**
→ Kill process: `lsof -ti:8000 | xargs kill -9` (backend)
→ Kill process: `lsof -ti:8501 | xargs kill -9` (frontend)

**API connection error in Streamlit?**
→ Make sure backend is running first!

## 🎉 You're Ready!

Start analyzing text, screening resumes, and detecting fake news!
