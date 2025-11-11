"""
Resume Screening Page
"""
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


st.set_page_config(page_title="Resume Screening", page_icon="📄", layout="wide")

API_URL = "http://localhost:8000/api"

st.title("📄 Resume Screening & Ranking")
st.markdown("Automate HR processes by screening and ranking resumes using AI.")

# Tabs
tab1, tab2 = st.tabs(["📋 Single Resume", "📊 Batch Ranking"])

# Tab 1: Single Resume Screening
with tab1:
    st.subheader("Screen a Single Resume")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Job Description**")
        job_description = st.text_area(
            "Enter job description:",
            placeholder="Enter the job requirements, responsibilities, and required skills...",
            height=300,
            key="jd_single"
        )
    
    with col2:
        st.markdown("**Resume**")
        resume_text = st.text_area(
            "Enter resume content:",
            placeholder="Paste the candidate's resume here...",
            height=300,
            key="resume_single"
        )
    
    if st.button("🔍 Screen Resume", key="screen_single", type="primary"):
        if job_description and resume_text:
            with st.spinner("Screening resume..."):
                try:
                    response = requests.post(
                        f"{API_URL}/resume/screen",
                        json={
                            "resume_text": resume_text,
                            "job_description": job_description
                        }
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        st.markdown("---")
                        st.subheader("📊 Screening Results")
                        
                        # Metrics
                        col1, col2, col3, col4 = st.columns(4)
                        
                        # Recommendation color coding
                        rec_colors = {
                            "highly_recommended": "🟢",
                            "recommended": "🟡",
                            "maybe": "🟠",
                            "reject": "🔴"
                        }
                        
                        with col1:
                            st.metric("Match Score", f"{result['match_score']:.1f}%")
                        
                        with col2:
                            st.metric("Skills Found", result['skills_count'])
                        
                        with col3:
                            st.metric("Experience", f"{result['experience_years']} years")
                        
                        with col4:
                            rec = result['recommendation'].replace('_', ' ').title()
                            st.metric(
                                "Recommendation",
                                f"{rec_colors.get(result['recommendation'], '')} {rec}"
                            )
                        
                        # Match score gauge
                        fig = go.Figure(go.Indicator(
                            mode="gauge+number+delta",
                            value=result['match_score'],
                            domain={'x': [0, 1], 'y': [0, 1]},
                            title={'text': "Match Score"},
                            delta={'reference': 70},
                            gauge={
                                'axis': {'range': [0, 100]},
                                'bar': {'color': "darkblue"},
                                'steps': [
                                    {'range': [0, 30], 'color': "lightcoral"},
                                    {'range': [30, 50], 'color': "lightyellow"},
                                    {'range': [50, 70], 'color': "lightgreen"},
                                    {'range': [70, 100], 'color': "green"}
                                ],
                                'threshold': {
                                    'line': {'color': "red", 'width': 4},
                                    'thickness': 0.75,
                                    'value': 70
                                }
                            }
                        ))
                        
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Skills found
                        if result['skills_found']:
                            st.subheader("🔧 Skills Identified")
                            skills_text = ", ".join(result['skills_found'])
                            st.success(skills_text)
                        else:
                            st.warning("No matching skills found")
                        
                        # Recommendation explanation
                        st.info(f"""
                        **Recommendation Criteria:**
                        - **Highly Recommended**: Match score ≥ 70% and 5+ matching skills
                        - **Recommended**: Match score ≥ 50% and 3+ matching skills
                        - **Maybe**: Match score ≥ 30%
                        - **Reject**: Match score < 30%
                        """)
                    
                    else:
                        st.error(f"API Error: {response.status_code}")
                
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.warning("Please enter both job description and resume")

# Tab 2: Batch Ranking
with tab2:
    st.subheader("Rank Multiple Resumes")
    
    st.markdown("**Job Description**")
    job_description_batch = st.text_area(
        "Enter job description:",
        placeholder="Enter the job requirements...",
        height=200,
        key="jd_batch"
    )
    
    st.markdown("**Resumes**")
    st.info("Enter multiple resumes below. Each resume should be separated by '---'")
    
    resumes_input = st.text_area(
        "Enter resumes (separated by ---):",
        placeholder="Resume 1 content\n---\nResume 2 content\n---\nResume 3 content",
        height=300,
        key="resumes_batch"
    )
    
    # Sample data option
    if st.checkbox("Use sample resumes"):
        resumes_input = """Software Engineer with 5 years of Python and FastAPI experience. Expert in machine learning and NLP. Worked with Docker and AWS.
---
Data Scientist with 3 years experience. Skilled in Python, R, and SQL. Experience with neural networks and deep learning.
---
Web Developer with 2 years of JavaScript and React. Some Python knowledge. Built several e-commerce websites.
---
Senior ML Engineer with 8 years experience in Python, TensorFlow, PyTorch. Led multiple NLP projects. AWS certified."""
        
        job_description_batch = """Senior Python Developer needed with 5+ years experience. 
        Must have: Python, FastAPI, Machine Learning, NLP, Docker, AWS.
        Nice to have: PyTorch, TensorFlow, CI/CD experience."""
    
    if st.button("🔍 Rank All Resumes", key="rank_batch", type="primary"):
        if job_description_batch and resumes_input:
            # Split resumes
            resume_texts = [r.strip() for r in resumes_input.split('---') if r.strip()]
            
            if resume_texts:
                with st.spinner(f"Ranking {len(resume_texts)} resumes..."):
                    try:
                        # Prepare data
                        resumes_data = [
                            {"id": f"Resume_{i+1}", "text": text}
                            for i, text in enumerate(resume_texts)
                        ]
                        
                        response = requests.post(
                            f"{API_URL}/resume/rank",
                            json={
                                "resumes": resumes_data,
                                "job_description": job_description_batch
                            }
                        )
                        
                        if response.status_code == 200:
                            results = response.json()
                            results_df = pd.DataFrame(results)
                            
                            st.markdown("---")
                            st.subheader("🏆 Ranking Results")
                            
                            # Summary metrics
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                st.metric("Total Resumes", len(results))
                            
                            with col2:
                                highly_rec = sum(1 for r in results if r['recommendation'] == 'highly_recommended')
                                st.metric("Highly Recommended", highly_rec)
                            
                            with col3:
                                avg_score = sum(r['match_score'] for r in results) / len(results)
                                st.metric("Average Match Score", f"{avg_score:.1f}%")
                            
                            # Bar chart of match scores
                            fig_bar = px.bar(
                                results_df,
                                x='resume_id',
                                y='match_score',
                                color='recommendation',
                                title="Match Scores by Resume",
                                labels={'match_score': 'Match Score (%)', 'resume_id': 'Resume'},
                                color_discrete_map={
                                    'highly_recommended': '#4CAF50',
                                    'recommended': '#FFC107',
                                    'maybe': '#FF9800',
                                    'reject': '#F44336'
                                }
                            )
                            
                            st.plotly_chart(fig_bar, use_container_width=True)
                            
                            # Detailed results table
                            st.subheader("📋 Detailed Rankings")
                            
                            # Format for display
                            display_df = results_df.copy()
                            display_df['skills_found'] = display_df['skills_found'].apply(lambda x: ', '.join(x) if x else 'None')
                            display_df['recommendation'] = display_df['recommendation'].str.replace('_', ' ').str.title()
                            
                            # Color code by rank
                            def highlight_top(row):
                                if row['rank'] == 1:
                                    return ['background-color: #C8E6C9'] * len(row)
                                elif row['rank'] <= 3:
                                    return ['background-color: #E3F2FD'] * len(row)
                                else:
                                    return [''] * len(row)
                            
                            styled_df = display_df.style.apply(highlight_top, axis=1)
                            st.dataframe(styled_df, use_container_width=True)
                            
                            # Download results
                            csv = results_df.to_csv(index=False)
                            st.download_button(
                                label="📥 Download Rankings as CSV",
                                data=csv,
                                file_name="resume_rankings.csv",
                                mime="text/csv"
                            )
                        
                        else:
                            st.error(f"API Error: {response.status_code}")
                    
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
            else:
                st.warning("Please enter at least one resume")
        else:
            st.warning("Please enter job description and resumes")

# Sidebar
with st.sidebar:
    st.header("ℹ️ About Resume Screening")
    st.info("""
    **Resume Screening** uses NLP to automatically evaluate and rank candidates.
    
    **Features:**
    - TF-IDF based similarity matching
    - Automatic skills extraction
    - Experience years detection
    - Intelligent ranking
    
    **Benefits:**
    - Save 60%+ screening time
    - Reduce bias in initial screening
    - Identify top candidates quickly
    - Standardized evaluation process
    """)
    
    st.header("💡 Tips")
    st.markdown("""
    - Include specific skills in job description
    - Use clear, descriptive language
    - Specify required years of experience
    - Review top-ranked candidates manually
    """)
    
    if st.button("🏠 Back to Home"):
        st.switch_page("app.py")
