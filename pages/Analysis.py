"""
Analysis page for E-commerce Analytics Application
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
    page_title="Analysis",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for compact layout
st.markdown("""
<style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    
    .main-title {
        font-size: 2.2rem;
        font-weight: 600;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 1.5rem;
    }
    
    .section-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #333;
        margin-bottom: 1rem;
        margin-top: 1.5rem;
    }
    
    .example-box {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        border-left: 4px solid #17a2b8;
    }
    
    .result-box {
        background-color: #e8f5e8;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #28a745;
        margin-bottom: 1rem;
    }
    
    .stButton > button {
        width: 100%;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'current_question' not in st.session_state:
        st.session_state.current_question = ""
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None
    if 'db_connected' not in st.session_state:
        st.session_state.db_connected = False

def check_database_connection():
    """Check and cache database connection status."""
    if not st.session_state.db_connected:
        with st.spinner("Connecting to database..."):
            try:
                connection_status = test_connection()
                st.session_state.db_connected = connection_status
                if not connection_status:
                    st.error("Database connection failed. Please check your configuration.")
                    return False
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
        with st.spinner("Analyzing your question..."):
            query_result = sql_agent.generate_sql(question)
        
        if not query_result.success:
            st.error(f"Analysis failed: {query_result.error}")
            return
        
        # Get column names from query result or generate them
        if query_result.columns:
            query_columns = query_result.columns
        else:
            # Fallback: generate generic column names based on actual data structure
            actual_column_count = len(query_result.data[0]) if query_result.data else 0
            query_columns = [f'column_{i+1}' for i in range(actual_column_count)]
        
        # Create story from results
        with st.spinner("Generating insights..."):
            story = story_generator.generate_story(
                question, 
                query_result.query, 
                query_result.data, 
                query_columns
            )
        
        # Store results in session state
        st.session_state.analysis_results = {
            'question': question,
            'query': query_result.query,
            'data': query_result.data,
            'columns': query_columns,
            'story': story
        }
        
        st.success("Analysis completed successfully!")
        
    except Exception as e:
        st.error(f"Analysis failed: {str(e)}")

def display_chat_interface():
    """Display the chat interface."""
    st.markdown('<div class="main-title">Ask Your Question</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Type your business question in plain English</div>', unsafe_allow_html=True)
    
    # Check database connection
    if not check_database_connection():
        return
    
    # Quick example questions
    st.markdown('<div class="section-title">Popular Questions</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    example_questions = [
        "What are our top-selling product categories?",
        "Show me monthly sales trends for 2023",
        "Which states generate the most revenue?",
        "What's the average order value by payment method?",
        "Which products have the highest return rates?",
        "Show me seasonal patterns in our sales data"
    ]
    
    for i, question in enumerate(example_questions):
        with col1 if i % 2 == 0 else col2:
            if st.button(question, key=f"example_{i}"):
                st.session_state.current_question = question
                st.rerun()
    
    # Question input
    st.markdown('<div class="section-title">Your Question</div>', unsafe_allow_html=True)
    
    question = st.text_area(
        "Enter your question:",
        value=st.session_state.current_question,
        height=100,
        placeholder="e.g., 'What are our top-selling products this year?'",
        key="question_input"
    )
    
    # Action buttons
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.button("Analyze Question", type="primary"):
            if question.strip():
                st.session_state.current_question = question.strip()
                st.session_state.messages.append({
                    "role": "user",
                    "content": question.strip()
                })
                
                # Perform analysis
                perform_analysis(question.strip())
                
                # Add assistant response
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "Analysis completed! Check the Results tab for detailed insights."
                })
                st.rerun()
            else:
                st.warning("Please enter a question first.")
    
    with col2:
        if st.button("Clear"):
            st.session_state.current_question = ""
            st.rerun()
    
    # Chat history
    if st.session_state.messages:
        st.markdown('<div class="section-title">Recent Questions</div>', unsafe_allow_html=True)
        
        # Show only last 5 messages
        recent_messages = st.session_state.messages[-5:]
        
        for message in recent_messages:
            if message["role"] == "user":
                st.markdown(f"**Q:** {message['content']}")
            else:
                st.markdown(f"**A:** {message['content']}")
        
        if st.button("Clear History"):
            st.session_state.messages = []
            st.rerun()

def display_analysis_results():
    """Display the analysis results."""
    if not st.session_state.analysis_results:
        return
    
    results = st.session_state.analysis_results
    story = results['story']
    data = results['data']
    columns = results['columns']
    
    # Question being analyzed
    st.markdown('<div class="result-box">', unsafe_allow_html=True)
    st.markdown(f"**Question:** {results['question']}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Executive Summary
    st.markdown('<div class="section-title">Executive Summary</div>', unsafe_allow_html=True)
    st.info(story.executive_summary)
    
    # Visualization
    st.markdown('<div class="section-title">Visualization</div>', unsafe_allow_html=True)
    try:
        chart_generator = get_chart_generator()
        fig = chart_generator.auto_generate_chart(data, columns, results['question'])
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Visualization error: {e}")
    
    # Key insights in two columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="section-title">Key Insights</div>', unsafe_allow_html=True)
        for insight in story.key_insights:
            st.markdown(f"• {insight}")
    
    with col2:
        st.markdown('<div class="section-title">Recommendations</div>', unsafe_allow_html=True)
        for i, rec in enumerate(story.recommendations, 1):
            st.markdown(f"{i}. {rec}")
    
    # Detailed Analysis
    st.markdown('<div class="section-title">Detailed Analysis</div>', unsafe_allow_html=True)
    st.markdown(story.detailed_analysis)
    
    # Data table
    with st.expander("View Raw Data"):
        if data:
            df = pd.DataFrame(data, columns=columns)
            st.dataframe(df, use_container_width=True)
            st.caption(f"SQL Query: {results['query']}")
    
    # Follow-up questions
    if story.follow_up_questions:
        st.markdown('<div class="section-title">Follow-up Questions</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        for i, question in enumerate(story.follow_up_questions):
            with col1 if i % 2 == 0 else col2:
                if st.button(question, key=f"followup_{hash(question)}"):
                    st.session_state.current_question = question
                    st.rerun()

def display_results_interface():
    """Display the results interface."""
    st.markdown('<div class="main-title">Analysis Results</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Insights and visualizations for your questions</div>', unsafe_allow_html=True)
    
    # Check if there are analysis results
    if st.session_state.analysis_results:
        display_analysis_results()
        return
    
    # No results yet
    st.info("No analysis results yet. Ask a question in the **Ask Questions** tab to see results here.")
    
    # Show current question if any
    if st.session_state.current_question:
        st.markdown('<div class="section-title">Current Question</div>', unsafe_allow_html=True)
        st.markdown(f"**Question:** {st.session_state.current_question}")
        
        if st.button("Analyze This Question", type="primary"):
            perform_analysis(st.session_state.current_question)
            st.rerun()

def main():
    """Main analysis page function."""
    # Initialize session state
    initialize_session_state()
    
    # Create tabs
    tab1, tab2 = st.tabs(["Ask Questions", "View Results"])
    
    with tab1:
        display_chat_interface()
    
    with tab2:
        display_results_interface()

if __name__ == "__main__":
    main()