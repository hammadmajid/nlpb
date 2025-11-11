# NLP for Business Intelligence 📊

A comprehensive NLP platform for business intelligence featuring sentiment analysis, resume screening, and fake news detection. Built with FastAPI and Streamlit for rapid MVP development.

## 🎯 Features

### 1. Sentiment Analysis 💬

- Analyze customer reviews and feedback
- Batch processing from CSV files
- Real-time sentiment scoring (polarity, subjectivity, confidence)
- Interactive visualizations and statistics
- Export results for further analysis

### 2. Resume Screening 📄

- Automated resume evaluation against job descriptions
- TF-IDF based similarity matching
- Automatic skills extraction
- Experience years detection
- Batch resume ranking
- Time-saving HR automation (60%+ faster screening)

### 3. Fake News Detection 🔍

- Clickbait pattern detection
- Hate speech identification
- Credibility scoring
- Source verification
- Comprehensive content analysis
- Brand protection and content moderation

## 🏗️ Architecture

```sh
nlpb/
├── backend/              # FastAPI backend service
│   ├── api/             # API endpoints and routes
│   ├── core/            # Core configuration
│   ├── models/          # Pydantic schemas
│   └── services/        # Business logic (NLP models)
├── frontend/            # Streamlit dashboard
│   ├── pages/          # Dashboard pages
│   └── app.py          # Main Streamlit app
├── data/               # Data storage
│   ├── samples/        # Sample datasets
│   └── uploads/        # User uploads
├── notebooks/          # Jupyter notebooks for experimentation
└── tests/             # Test suites
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10+ (but < 3.14)
- uv (Python package manager)

### Installation

1. **Clone or navigate to the project:**

```bash
cd ~/Code/nlpb
```

2. **Install dependencies:**

```bash
uv sync
```

This will install all required packages including:

- FastAPI & Uvicorn (API backend)
- Streamlit (Dashboard UI)
- TextBlob (NLP processing)
- Scikit-learn (ML algorithms)
- Pandas & NumPy (Data processing)
- Plotly (Visualizations)

3. **Download TextBlob corpora:**

```bash
uv run python -c "import nltk; nltk.download('brown'); nltk.download('punkt')"
```

### Running the Application

#### Terminal 1 - Start Backend API

```bash
cd ~/Code/nlpb
uv run python backend/main.py
```

The API will be available at: <http://localhost:8000>

- API Documentation: <http://localhost:8000/docs>
- Health Check: <http://localhost:8000/health>

#### Terminal 2 - Start Streamlit Dashboard

```bash
cd ~/Code/nlpb
uv run streamlit run frontend/app.py
```

The dashboard will open automatically at: <http://localhost:8501>

## 📖 Usage Guide

### Sentiment Analysis

**Single Text Analysis:**

1. Navigate to "Sentiment Analysis" page
2. Enter customer review or feedback
3. Click "Analyze"
4. View sentiment metrics and visualizations

**Batch Analysis:**

1. Prepare CSV file with a 'text' column
2. Upload file or use sample data
3. Click "Analyze All"
4. View aggregate statistics and download results

### Resume Screening

**Single Resume:**

1. Navigate to "Resume Screening" page
2. Enter job description and resume text
3. Click "Screen Resume"
4. Review match score, skills, and recommendation

**Batch Ranking:**

1. Enter job description
2. Add multiple resumes (separated by ---)
3. Click "Rank All Resumes"
4. View ranked results and download CSV

### Fake News Detection

1. Navigate to "Fake News Detection" page
2. Paste article or social media content
3. Optionally add source information
4. Click "Analyze Content"
5. Review fake news probability, credibility score, and warnings

## 🔧 API Endpoints

### Sentiment Analysis

- `POST /api/sentiment/analyze` - Analyze single text
- `POST /api/sentiment/batch` - Batch analysis
- `POST /api/sentiment/statistics` - Get aggregate statistics

### Resume Screening

- `POST /api/resume/screen` - Screen single resume
- `POST /api/resume/rank` - Rank multiple resumes

### Fake News Detection

- `POST /api/fakenews/detect` - Detect fake news and harmful content

### Health Check

- `GET /` - Root endpoint
- `GET /health` - Health check

## 🧪 Testing

Run the test suite:

```bash
cd ~/Code/nlpb
uv run pytest tests/ -v
```

## 📊 MVP Business Logic

### Sentiment Analysis

- **Technology**: TextBlob for polarity and subjectivity analysis
- **Metrics**: Polarity (-1 to +1), Subjectivity (0 to 1), Confidence
- **Classification**: Positive, Neutral, Negative
- **Use Case**: Customer satisfaction, brand monitoring

### Resume Screening

- **Technology**: TF-IDF vectorization + Cosine similarity
- **Features**: Skills extraction, experience detection
- **Scoring**: 0-100% match score with job description
- **Recommendations**: Highly Recommended, Recommended, Maybe, Reject

### Fake News Detection

- **Components**:
  - Clickbait detection (sensational words, punctuation patterns)
  - Hate speech detection (offensive language patterns)
  - Credibility scoring (source reputation, citations, quotes)
- **Output**: Fake news probability, detailed risk scores, warnings

## 🎓 Research Background

This project implements concepts from:

- NLP for Business Intelligence research
- Sentiment analysis for business reviews
- Automated resume screening with AI
- Fake news and hate speech detection using NLP

## 🛣️ Future Enhancements

### Short Term

- [ ] Add user authentication
- [ ] Implement data persistence (database)
- [ ] Add more NLP models (BERT, RoBERTa)
- [ ] Enhanced visualizations
- [ ] API rate limiting

### Long Term

- [ ] Deep learning models for better accuracy
- [ ] Real-time data streaming
- [ ] Multi-language support
- [ ] Integration with BI tools (Tableau, Power BI)
- [ ] Advanced topic modeling
- [ ] Automated report generation

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write/update tests
5. Submit a pull request

## 📝 License

This project is for educational and research purposes.

## 🐛 Troubleshooting

### Backend API not starting

- Check if port 8000 is available
- Ensure all dependencies are installed: `uv sync`
- Check Python version: `python --version` (should be 3.10-3.13)

### Streamlit connection error

- Ensure backend API is running first
- Check API URL in Streamlit pages (default: <http://localhost:8000>)
- Verify CORS settings in backend/core/config.py

### Import errors

- Run: `uv sync` to install/update dependencies
- Download NLTK data: `uv run python -c "import nltk; nltk.download('brown'); nltk.download('punkt')"`

## 📞 Support

For issues, questions, or contributions:

- Open an issue on the repository
- Check the documentation
- Review the API documentation at <http://localhost:8000/docs>

## 🙏 Acknowledgments

Built with:

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [Streamlit](https://streamlit.io/) - Data app framework
- [TextBlob](https://textblob.readthedocs.io/) - NLP library
- [Scikit-learn](https://scikit-learn.org/) - Machine learning library
- [Plotly](https://plotly.com/) - Interactive visualizations

---

**Version**: 0.1.0
**Status**: MVP Ready
**Last Updated**: 2025-11-11
