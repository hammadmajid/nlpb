"""
Sentiment Analysis Page
"""
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import StringIO


st.set_page_config(page_title="Sentiment Analysis", page_icon="💬", layout="wide")

# API endpoint
API_URL = "http://localhost:8000/api"

st.title("💬 Sentiment Analysis")
st.markdown("Analyze customer reviews and feedback to understand sentiment trends.")

# Tabs for different input methods
tab1, tab2 = st.tabs(["📝 Single Text", "📊 Batch Analysis"])

# Tab 1: Single Text Analysis
with tab1:
    st.subheader("Analyze Single Review or Feedback")
    
    text_input = st.text_area(
        "Enter text to analyze:",
        placeholder="Type or paste customer review, feedback, or any text...",
        height=150
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        analyze_button = st.button("🔍 Analyze", key="single_analyze", type="primary")
    
    if analyze_button and text_input:
        with st.spinner("Analyzing sentiment..."):
            try:
                response = requests.post(
                    f"{API_URL}/sentiment/analyze",
                    json={"text": text_input}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Display results
                    st.markdown("---")
                    st.subheader("📈 Analysis Results")
                    
                    # Metrics row
                    col1, col2, col3, col4 = st.columns(4)
                    
                    # Sentiment color coding
                    sentiment_colors = {
                        "positive": "🟢",
                        "neutral": "🟡",
                        "negative": "🔴"
                    }
                    
                    with col1:
                        st.metric(
                            "Sentiment",
                            f"{sentiment_colors.get(result['sentiment'], '')} {result['sentiment'].upper()}"
                        )
                    
                    with col2:
                        st.metric("Polarity", f"{result['polarity']:.3f}")
                    
                    with col3:
                        st.metric("Subjectivity", f"{result['subjectivity']:.3f}")
                    
                    with col4:
                        st.metric("Confidence", f"{result['confidence']:.3f}")
                    
                    # Visualization
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=result['polarity'],
                        domain={'x': [0, 1], 'y': [0, 1]},
                        title={'text': "Sentiment Polarity"},
                        gauge={
                            'axis': {'range': [-1, 1]},
                            'bar': {'color': "darkblue"},
                            'steps': [
                                {'range': [-1, -0.1], 'color': "lightcoral"},
                                {'range': [-0.1, 0.1], 'color': "lightyellow"},
                                {'range': [0.1, 1], 'color': "lightgreen"}
                            ],
                            'threshold': {
                                'line': {'color': "red", 'width': 4},
                                'thickness': 0.75,
                                'value': 0
                            }
                        }
                    ))
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Interpretation
                    st.info(f"""
                    **Interpretation:**
                    - **Polarity** ranges from -1 (most negative) to +1 (most positive)
                    - **Subjectivity** ranges from 0 (objective) to 1 (subjective)
                    - **Confidence** indicates how strong the sentiment is (0 to 1)
                    """)
                    
                else:
                    st.error(f"API Error: {response.status_code} - {response.text}")
            
            except Exception as e:
                st.error(f"Error connecting to API: {str(e)}")
                st.info("Make sure the backend API is running on http://localhost:8000")

# Tab 2: Batch Analysis
with tab2:
    st.subheader("Analyze Multiple Reviews")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload CSV file with reviews (must have a 'text' column)",
        type=['csv']
    )
    
    # Sample data option
    if st.checkbox("Use sample data"):
        sample_data = """text
This product is amazing! Best purchase ever.
The service was okay, nothing special.
Terrible experience, would not recommend.
Love it! Exceeded my expectations.
Average quality, could be better.
Worst product I've ever bought.
"""
        uploaded_file = StringIO(sample_data)
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            
            if 'text' not in df.columns:
                st.error("CSV must contain a 'text' column")
            else:
                st.write(f"Loaded {len(df)} reviews")
                st.dataframe(df.head(), use_container_width=True)
                
                if st.button("🔍 Analyze All", key="batch_analyze", type="primary"):
                    with st.spinner(f"Analyzing {len(df)} reviews..."):
                        try:
                            texts = df['text'].tolist()
                            
                            # Get batch results
                            response = requests.post(
                                f"{API_URL}/sentiment/batch",
                                json={"texts": texts}
                            )
                            
                            if response.status_code == 200:
                                results = response.json()
                                results_df = pd.DataFrame(results)
                                
                                # Get statistics
                                stats_response = requests.post(
                                    f"{API_URL}/sentiment/statistics",
                                    json={"texts": texts}
                                )
                                
                                if stats_response.status_code == 200:
                                    stats = stats_response.json()
                                    
                                    # Display statistics
                                    st.markdown("---")
                                    st.subheader("📊 Overall Statistics")
                                    
                                    col1, col2, col3, col4 = st.columns(4)
                                    
                                    with col1:
                                        st.metric("Total Reviews", stats['total_reviews'])
                                    
                                    with col2:
                                        st.metric("🟢 Positive", f"{stats['positive_count']} ({stats['positive_percentage']:.1f}%)")
                                    
                                    with col3:
                                        st.metric("🟡 Neutral", f"{stats['neutral_count']} ({stats['neutral_percentage']:.1f}%)")
                                    
                                    with col4:
                                        st.metric("🔴 Negative", f"{stats['negative_count']} ({stats['negative_percentage']:.1f}%)")
                                    
                                    # Pie chart
                                    fig_pie = px.pie(
                                        values=[stats['positive_count'], stats['neutral_count'], stats['negative_count']],
                                        names=['Positive', 'Neutral', 'Negative'],
                                        title="Sentiment Distribution",
                                        color_discrete_map={
                                            'Positive': '#4CAF50',
                                            'Neutral': '#FFC107',
                                            'Negative': '#F44336'
                                        }
                                    )
                                    
                                    st.plotly_chart(fig_pie, use_container_width=True)
                                    
                                    # Histogram of polarity
                                    fig_hist = px.histogram(
                                        results_df,
                                        x='polarity',
                                        nbins=30,
                                        title="Polarity Distribution",
                                        labels={'polarity': 'Sentiment Polarity'},
                                        color_discrete_sequence=['#1E88E5']
                                    )
                                    
                                    st.plotly_chart(fig_hist, use_container_width=True)
                                    
                                    # Detailed results
                                    st.subheader("📋 Detailed Results")
                                    st.dataframe(results_df, use_container_width=True)
                                    
                                    # Download button
                                    csv = results_df.to_csv(index=False)
                                    st.download_button(
                                        label="📥 Download Results as CSV",
                                        data=csv,
                                        file_name="sentiment_analysis_results.csv",
                                        mime="text/csv"
                                    )
                            
                            else:
                                st.error(f"API Error: {response.status_code}")
                        
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
        
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")

# Sidebar
with st.sidebar:
    st.header("ℹ️ About Sentiment Analysis")
    st.info("""
    **Sentiment Analysis** uses NLP to determine the emotional tone of text.
    
    **Use Cases:**
    - Customer review analysis
    - Social media monitoring
    - Brand perception tracking
    - Customer satisfaction measurement
    
    **Metrics Explained:**
    - **Polarity**: -1 (negative) to +1 (positive)
    - **Subjectivity**: 0 (objective) to 1 (subjective)
    - **Confidence**: Strength of sentiment (0 to 1)
    """)
    
    if st.button("🏠 Back to Home"):
        st.switch_page("app.py")
