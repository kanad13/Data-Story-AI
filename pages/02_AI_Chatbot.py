"""
AI Chatbot page for Data Story AI Application
Implements dropdown interface matching good-layout.png design
"""

import streamlit as st
import pandas as pd
import logging
from typing import Optional, Dict, Any
import sys
from pathlib import Path

# Add paths for custom modules
sys.path.append(str(Path(__file__).parent.parent / "30-database"))
sys.path.append(str(Path(__file__).parent.parent / "40-llm"))
sys.path.append(str(Path(__file__).parent.parent / "50-visualization"))

try:
    from connection import get_database, test_connection
    from schema import get_schema
    from sql_agent import get_sql_agent
    from story_generator import get_story_generator
    from plotly_charts import get_chart_generator
except ImportError as e:
    st.error("Required modules not available. Please check your installation.")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for clean layout matching good-layout.png
st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 3rem;
        padding-right: 3rem;
        max-width: 1200px;
    }
    
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .subtitle {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .question-section {
        background-color: #f8f9fa;
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        border: 1px solid #dee2e6;
    }
    
    .stSelectbox > div > div {
        background-color: white;
        border: 2px solid #dee2e6;
        border-radius: 8px;
        padding: 0.5rem;
    }
    
    .stSelectbox > div > div:focus {
        border-color: #1f77b4;
        box-shadow: 0 0 0 0.2rem rgba(31, 119, 180, 0.25);
    }
    
    .custom-text-area textarea {
        border: 2px solid #dee2e6 !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        font-size: 1rem !important;
        background-color: white !important;
    }
    
    .custom-text-area textarea:focus {
        border-color: #1f77b4 !important;
        box-shadow: 0 0 0 0.2rem rgba(31, 119, 180, 0.25) !important;
    }
    
    .stButton > button {
        background-color: #1f77b4;
        color: white;
        border: none;
        padding: 12px 30px;
        border-radius: 8px;
        font-size: 1.1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
        margin-top: 1rem;
    }
    
    .stButton > button:hover {
        background-color: #1565c0;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(31, 119, 180, 0.3);
    }
    
    .results-section {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        margin-top: 2rem;
        border: 1px solid #dee2e6;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .result-header {
        background-color: #e8f5e8;
        padding: 1.5rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        border-left: 5px solid #4caf50;
    }
    
    .insight-box {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        border-left: 4px solid #17a2b8;
    }
    
    .recommendation-box {
        background: #fff3e0;
        padding: 1.5rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        border-left: 4px solid #ff9800;
    }
    
    .loading-spinner {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 2rem;
    }
    
    .section-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #333;
        margin-bottom: 1rem;
        margin-top: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if 'current_question' not in st.session_state:
        st.session_state.current_question = ""
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None
    if 'db_connected' not in st.session_state:
        st.session_state.db_connected = False
    if 'custom_question' not in st.session_state:
        st.session_state.custom_question = ""

def check_database_connection():
    """Check and cache database connection status."""
    if not st.session_state.db_connected:
        try:
            connection_status = test_connection()
            st.session_state.db_connected = connection_status
            return connection_status
        except Exception as e:
            st.error(f"Database connection error: {e}")
            st.session_state.db_connected = False
            return False
    return st.session_state.db_connected

def perform_analysis(question: str):
    """Perform comprehensive analysis of a business question."""
    try:
        # Initialize components
        sql_agent = get_sql_agent()
        story_generator = get_story_generator()
        chart_generator = get_chart_generator()
        
        # Generate and execute SQL query
        with st.spinner("🔍 Analyzing your question..."):
            query_result = sql_agent.generate_sql(question)
        
        if not query_result.success:
            st.error(f"❌ Analysis failed: {query_result.error}")
            return False
        
        # Get column names from query result
        if query_result.columns:
            query_columns = query_result.columns
        else:
            actual_column_count = len(query_result.data[0]) if query_result.data else 0
            query_columns = [f'column_{i+1}' for i in range(actual_column_count)]
        
        # Create story from results
        with st.spinner("📖 Generating insights..."):
            story = story_generator.generate_story(
                question, 
                query_result.query, 
                query_result.data, 
                query_columns
            )
        
        # Store results in session state
        results = {
            'question': question,
            'query': query_result.query,
            'data': query_result.data,
            'columns': query_columns,
            'story': story
        }
        
        st.session_state.analysis_results = results
        return True
        
    except Exception as e:
        st.error(f"❌ Analysis failed: {str(e)}")
        return False

def display_analysis_results():
    """Display the analysis results in a clean format."""
    if not st.session_state.analysis_results:
        return
    
    results = st.session_state.analysis_results
    story = results['story']
    data = results['data']
    columns = results['columns']
    
    # Results container
    st.markdown('<div class="results-section">', unsafe_allow_html=True)
    
    # Question being analyzed
    st.markdown(f"""
    <div class="result-header">
        <h3>📋 Question Analyzed</h3>
        <p style="font-size: 1.1rem; margin: 0;"><strong>"{results['question']}"</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Executive Summary
    st.markdown('<div class="section-title">📊 Executive Summary</div>', unsafe_allow_html=True)
    st.info(story.executive_summary)
    
    # Visualization
    st.markdown('<div class="section-title">📈 Data Visualization</div>', unsafe_allow_html=True)
    try:
        chart_generator = get_chart_generator()
        fig = chart_generator.auto_generate_chart(data, columns, results['question'])
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Visualization error: {e}")
    
    # Key insights and recommendations in columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="section-title">💡 Key Insights</div>', unsafe_allow_html=True)
        for i, insight in enumerate(story.key_insights, 1):
            st.markdown(f"""
            <div class="insight-box">
                <strong>{i}.</strong> {insight}
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="section-title">🎯 Recommendations</div>', unsafe_allow_html=True)
        for i, rec in enumerate(story.recommendations, 1):
            st.markdown(f"""
            <div class="recommendation-box">
                <strong>{i}.</strong> {rec}
            </div>
            """, unsafe_allow_html=True)
    
    # Detailed Analysis
    st.markdown('<div class="section-title">📝 Detailed Analysis</div>', unsafe_allow_html=True)
    st.markdown(story.detailed_analysis)
    
    # Data table
    with st.expander("📋 View Raw Data & SQL Query"):
        if data:
            df = pd.DataFrame(data, columns=columns)
            st.dataframe(df, use_container_width=True)
            st.code(results['query'], language='sql')
    
    # Follow-up questions
    if story.follow_up_questions:
        st.markdown('<div class="section-title">❓ Suggested Follow-up Questions</div>', unsafe_allow_html=True)
        
        for i, question in enumerate(story.follow_up_questions):
            if st.button(f"🔍 {question}", key=f"followup_{i}"):
                st.session_state.current_question = question
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    """Main AI Chatbot page function."""
    # Initialize session state
    initialize_session_state()
    
    # Header
    st.markdown('<div class="main-title">AI Data Story Chatbot</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Ask questions about E-commerce data and get instant AI-powered insights</div>', unsafe_allow_html=True)
    
    # Check database connection
    if not check_database_connection():
        st.error("❌ Database connection failed. Please check your configuration.")
        return
    
    # Question Selection Section
    st.markdown('<div class="question-section">', unsafe_allow_html=True)
    
    # Predefined questions for dropdown (matching your design)
    predefined_questions = [
        "Select a question",
        "What are our top-selling product categories?",
        "Show me monthly sales trends for 2023",
        "Which states generate the most revenue?",
        "What's the average order value by payment method?",
        "Which products have the highest profit margins?",
        "Show me seasonal patterns in our sales data",
        "How do customer preferences vary by geography?",
        "What are the most popular products in each category?",
        "Other (Type your own question)"
    ]
    
    st.markdown("**Choose a question or select 'Other' to type your own:**")
    
    # Question dropdown selector
    selected_question = st.selectbox(
        "",
        predefined_questions,
        index=0,
        key="question_selector"
    )
    
    # Handle custom question input
    if selected_question == "Other (Type your own question)":
        st.markdown("**Enter your custom question:**")
        custom_question = st.text_area(
            "",
            placeholder="e.g., 'What are the trends in customer acquisition by quarter?'",
            height=100,
            key="custom_question_input"
        )
        current_question = custom_question.strip() if custom_question.strip() else ""
    elif selected_question != "Select a question":
        current_question = selected_question
    else:
        current_question = ""
    
    # Analyze button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Analyze Question", disabled=not current_question, use_container_width=True):
            if current_question:
                st.session_state.current_question = current_question
                if perform_analysis(current_question):
                    st.success("✅ Analysis completed successfully!")
                    st.rerun()
            else:
                st.warning("⚠️ Please select or enter a question first.")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Display results if available
    if st.session_state.analysis_results:
        display_analysis_results()
    else:
        # Show example of what users can expect
        st.markdown("""
        <div style="text-align: center; padding: 3rem; color: #666;">
            <h3>👆 Select a question above to see AI-powered data stories in action</h3>
            <p>Our AI will analyze your question, generate SQL queries, and provide comprehensive insights with visualizations, key findings, and actionable recommendations.</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()