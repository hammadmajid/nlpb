"""
Main Streamlit application for NLP Business Intelligence Dashboard.
"""
import streamlit as st


# Page configuration
st.set_page_config(
    page_title="NLP Business Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 2rem;
    }
    .feature-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        color: #000;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Main page
st.markdown('<h1 class="main-header">📊 NLP Business Intelligence Dashboard</h1>', unsafe_allow_html=True)

st.markdown("""
Welcome to the **NLP Business Intelligence** platform! This application provides powerful
Natural Language Processing tools for business decision-making.
""")

# Feature cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h3>💬 Sentiment Analysis</h3>
        <p>Analyze customer reviews and feedback to understand sentiment trends and improve customer satisfaction.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Go to Sentiment Analysis", key="sentiment", use_container_width=True):
        st.switch_page("pages/1_sentiment_analysis.py")

with col2:
    st.markdown("""
    <div class="feature-card">
        <h3>📄 Resume Screening</h3>
        <p>Automate HR processes by screening and ranking resumes against job descriptions using AI.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Go to Resume Screening", key="resume", use_container_width=True):
        st.switch_page("pages/2_resume_screening.py")

with col3:
    st.markdown("""
    <div class="feature-card">
        <h3>🔍 Fake News Detection</h3>
        <p>Detect fake news, clickbait, and hate speech to protect brand reputation and ensure content quality.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Go to Fake News Detection", key="fakenews", use_container_width=True):
        st.switch_page("pages/3_fake_news_detection.py")

# Instructions
st.markdown("---")
st.subheader("📖 How to Use")

instructions = """
1. **Select a Feature**: Click on one of the feature cards above to access the specific tool
2. **Input Your Data**: Enter text, upload files, or paste content depending on the feature
3. **Analyze**: Click the analyze button to process your data using NLP models
4. **View Results**: Explore visualizations, metrics, and detailed insights
5. **Export**: Download results for further analysis or reporting

### Features Overview:

**Sentiment Analysis**
- Single text analysis
- Batch processing from CSV
- Statistical summaries
- Interactive visualizations

**Resume Screening**
- Single resume evaluation
- Batch resume ranking
- Skills extraction
- Match score calculation

**Fake News Detection**
- Clickbait detection
- Hate speech identification
- Credibility scoring
- Source verification
"""

st.markdown(instructions)

# Sidebar
with st.sidebar:
    st.header("ℹ️ About")
    st.info("""
    This platform leverages state-of-the-art NLP techniques to provide
    actionable business intelligence from unstructured text data.

    **Technologies:**
    - FastAPI
    - Streamlit
    - TextBlob
    - Scikit-learn
    - Pandas
    """)

    st.header("🚀 Quick Start")
    st.markdown("""
    1. Ensure backend API is running on port 8000
    2. Select a feature from the main page
    3. Follow the on-screen instructions
    """)

    st.header("📞 Support")
    st.markdown("""
    For issues or questions, please check the documentation or
    contact the development team.
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    NLP Business Intelligence Dashboard v0.1.0 | Built with FastAPI & Streamlit
</div>
""", unsafe_allow_html=True)
