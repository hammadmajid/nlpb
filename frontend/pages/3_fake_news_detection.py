"""
Fake News Detection Page
"""
import streamlit as st
import requests
import plotly.graph_objects as go


st.set_page_config(page_title="Fake News Detection", page_icon="🔍", layout="wide")

API_URL = "http://localhost:8000/api"

st.title("🔍 Fake News & Harmful Content Detection")
st.markdown("Detect fake news, clickbait, and hate speech to protect brand reputation.")

st.markdown("---")

# Input section
col1, col2 = st.columns([3, 1])

with col1:
    text_input = st.text_area(
        "Enter article or social media post:",
        placeholder="Paste the content you want to analyze...",
        height=200
    )

with col2:
    source_input = st.text_input(
        "Source (optional):",
        placeholder="e.g., BBC, Twitter, Unknown"
    )

if st.button("🔍 Analyze Content", type="primary", use_container_width=True):
    if text_input:
        with st.spinner("Analyzing content..."):
            try:
                response = requests.post(
                    f"{API_URL}/fakenews/detect",
                    json={
                        "text": text_input,
                        "source": source_input or ""
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    st.markdown("---")
                    st.subheader("📊 Analysis Results")
                    
                    # Main verdict
                    if result['is_fake_news']:
                        st.error("⚠️ **WARNING**: This content shows signs of being fake news or harmful content!")
                    else:
                        st.success("✅ This content appears to be legitimate")
                    
                    # Key metrics
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric(
                            "Fake News Probability",
                            f"{result['fake_news_probability']:.1f}%"
                        )
                    
                    with col2:
                        st.metric(
                            "Credibility Score",
                            f"{result['credibility_score']:.1f}%"
                        )
                    
                    with col3:
                        st.metric(
                            "Clickbait Score",
                            f"{result['clickbait_score']:.1f}%"
                        )
                    
                    with col4:
                        st.metric(
                            "Hate Speech Score",
                            f"{result['hate_score']:.1f}%"
                        )
                    
                    # Warnings
                    if result['warnings']:
                        st.markdown("### ⚠️ Warnings Detected")
                        for warning in result['warnings']:
                            st.warning(f"• {warning}")
                    
                    # Detailed scores visualization
                    st.markdown("---")
                    st.subheader("📈 Detailed Score Breakdown")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Fake News Probability Gauge
                        fig_fake = go.Figure(go.Indicator(
                            mode="gauge+number",
                            value=result['fake_news_probability'],
                            domain={'x': [0, 1], 'y': [0, 1]},
                            title={'text': "Fake News Probability"},
                            gauge={
                                'axis': {'range': [0, 100]},
                                'bar': {'color': "darkred"},
                                'steps': [
                                    {'range': [0, 30], 'color': "lightgreen"},
                                    {'range': [30, 60], 'color': "lightyellow"},
                                    {'range': [60, 100], 'color': "lightcoral"}
                                ],
                                'threshold': {
                                    'line': {'color': "red", 'width': 4},
                                    'thickness': 0.75,
                                    'value': 60
                                }
                            }
                        ))
                        st.plotly_chart(fig_fake, use_container_width=True)
                    
                    with col2:
                        # Credibility Score Gauge
                        fig_cred = go.Figure(go.Indicator(
                            mode="gauge+number",
                            value=result['credibility_score'],
                            domain={'x': [0, 1], 'y': [0, 1]},
                            title={'text': "Credibility Score"},
                            gauge={
                                'axis': {'range': [0, 100]},
                                'bar': {'color': "darkgreen"},
                                'steps': [
                                    {'range': [0, 30], 'color': "lightcoral"},
                                    {'range': [30, 60], 'color': "lightyellow"},
                                    {'range': [60, 100], 'color': "lightgreen"}
                                ],
                                'threshold': {
                                    'line': {'color': "green", 'width': 4},
                                    'thickness': 0.75,
                                    'value': 50
                                }
                            }
                        ))
                        st.plotly_chart(fig_cred, use_container_width=True)
                    
                    # Additional metrics bar chart
                    scores_data = {
                        'Metric': ['Clickbait', 'Hate Speech', 'Credibility (inverted)'],
                        'Score': [
                            result['clickbait_score'],
                            result['hate_score'],
                            100 - result['credibility_score']
                        ]
                    }
                    
                    fig_bar = go.Figure(data=[
                        go.Bar(
                            x=scores_data['Metric'],
                            y=scores_data['Score'],
                            marker_color=['orange', 'red', 'blue'],
                            text=scores_data['Score'],
                            texttemplate='%{text:.1f}%',
                            textposition='auto',
                        )
                    ])
                    
                    fig_bar.update_layout(
                        title="Risk Factor Scores",
                        yaxis_title="Score (%)",
                        yaxis_range=[0, 100],
                        showlegend=False
                    )
                    
                    st.plotly_chart(fig_bar, use_container_width=True)
                    
                    # Detailed analysis
                    st.markdown("---")
                    st.subheader("🔬 Detailed Analysis")
                    
                    with st.expander("📰 Clickbait Analysis"):
                        details = result['details']['clickbait']
                        st.write(f"**Is Clickbait:** {details['is_clickbait']}")
                        st.write(f"**Score:** {details['clickbait_score']:.1f}%")
                        st.write(f"**Exclamation marks:** {details['exclamation_count']}")
                        st.write(f"**CAPS ratio:** {details['caps_ratio']:.1%}")
                        if details['clickbait_words']:
                            st.write(f"**Clickbait words found:** {', '.join(details['clickbait_words'])}")
                    
                    with st.expander("😡 Hate Speech Analysis"):
                        details = result['details']['hate_speech']
                        st.write(f"**Contains Hate Speech:** {details['contains_hate_speech']}")
                        st.write(f"**Score:** {details['hate_score']:.1f}%")
                        st.write(f"**Offensive patterns found:** {details['offensive_patterns_found']}")
                        st.write(f"**Sentiment polarity:** {details['sentiment_polarity']:.3f}")
                    
                    with st.expander("✅ Credibility Analysis"):
                        details = result['details']['credibility']
                        st.write(f"**Is Credible:** {details['credible']}")
                        st.write(f"**Score:** {details['credibility_score']:.1f}%")
                        st.write(f"**Credible sources mentioned:** {details['credible_sources_mentioned']}")
                        st.write(f"**Has citations:** {details['has_citations']}")
                        st.write(f"**Has quotes:** {details['has_quotes']}")
                    
                    # Recommendations
                    st.markdown("---")
                    st.subheader("💡 Recommendations")
                    
                    if result['is_fake_news']:
                        st.error("""
                        **Action Required:**
                        - Verify information with credible sources
                        - Check for corroborating evidence
                        - Be cautious about sharing this content
                        - Consider flagging for review
                        """)
                    else:
                        st.info("""
                        **Good Practices:**
                        - Always verify important information
                        - Check the source reputation
                        - Look for citations and evidence
                        - Be aware of emotional manipulation
                        """)
                
                else:
                    st.error(f"API Error: {response.status_code}")
            
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.info("Make sure the backend API is running on http://localhost:8000")
    else:
        st.warning("Please enter some text to analyze")

# Sample content examples
st.markdown("---")
st.subheader("📚 Try Sample Content")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📰 News Article", use_container_width=True):
        st.session_state.sample_text = """
        A new study published by researchers at Stanford University has found that regular 
        exercise can significantly improve cognitive function in older adults. The research, 
        which was published in the Journal of Neuroscience, followed 500 participants over 
        two years and found that those who exercised for at least 30 minutes daily showed 
        improved memory and problem-solving skills.
        """
        st.rerun()

with col2:
    if st.button("🚨 Clickbait", use_container_width=True):
        st.session_state.sample_text = """
        YOU WON'T BELIEVE WHAT HAPPENED NEXT!!! This SHOCKING discovery will change 
        EVERYTHING you thought you knew!!! Scientists HATE this one simple trick!!!
        URGENT ALERT - Read this NOW before it's too late!!!
        """
        st.rerun()

with col3:
    if st.button("😡 Offensive Content", use_container_width=True):
        st.session_state.sample_text = """
        These people are so stupid and ignorant. They should all be eliminated from 
        society. I hate everyone who disagrees with me.
        """
        st.rerun()

# Sidebar
with st.sidebar:
    st.header("ℹ️ About Fake News Detection")
    st.info("""
    **Fake News Detection** helps identify misleading or harmful content.
    
    **Detection Features:**
    - Clickbait patterns
    - Hate speech indicators
    - Credibility assessment
    - Source verification
    
    **Use Cases:**
    - Social media monitoring
    - Content moderation
    - Brand protection
    - Fact-checking assistance
    """)
    
    st.header("🎯 Score Interpretation")
    st.markdown("""
    **Fake News Probability:**
    - 0-30%: Low risk
    - 30-60%: Medium risk
    - 60-100%: High risk
    
    **Credibility Score:**
    - 0-30%: Low credibility
    - 30-60%: Medium credibility
    - 60-100%: High credibility
    """)
    
    st.header("⚠️ Disclaimer")
    st.warning("""
    This is an automated tool and may not be 100% accurate. 
    Always verify important information with multiple sources.
    """)
    
    if st.button("🏠 Back to Home"):
        st.switch_page("app.py")

# Load sample if set
if 'sample_text' in st.session_state:
    st.info(f"Sample loaded. Click 'Analyze Content' to process it.")
