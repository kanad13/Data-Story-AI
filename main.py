"""
E-commerce Analytics Streamlit Application

A conversational data analytics tool that allows users to ask business questions
about e-commerce data and receive rich, multi-modal insights combining text
explanations, process diagrams, and interactive visualizations.
"""

import streamlit as st
import pandas as pd
import logging
from typing import Optional, Dict, Any
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import custom modules
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / "30-database"))
sys.path.append(str(Path(__file__).parent / "40-llm"))
sys.path.append(str(Path(__file__).parent / "50-visualization"))

try:
    from connection import get_database, test_connection
    from schema import get_schema
    from sql_agent import get_sql_agent
    from story_generator import get_story_generator
    from plotly_charts import get_chart_generator
except ImportError as e:
    logger.error(f"Failed to import modules: {e}")
    st.error("Required modules not available. Please check your installation.")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="E-commerce Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .status-success {
        color: #28a745;
        font-weight: 600;
    }
    .status-error {
        color: #dc3545;
        font-weight: 600;
    }
    .chat-input {
        background-color: #ffffff;
        border: 2px solid #e0e0e0;
        border-radius: 0.5rem;
        padding: 1rem;
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
    if 'llm_ready' not in st.session_state:
        st.session_state.llm_ready = False

def check_database_connection():
    """Check and cache database connection status."""
    if not st.session_state.db_connected:
        with st.spinner("Connecting to database..."):
            try:
                connection_status = test_connection()
                st.session_state.db_connected = connection_status
                if connection_status:
                    logger.info("Database connection successful")
                else:
                    logger.error("Database connection failed")
            except Exception as e:
                logger.error(f"Database connection error: {e}")
                st.session_state.db_connected = False
    
    return st.session_state.db_connected

def perform_analysis(question: str):
    """
    Perform comprehensive analysis of a business question.
    
    Args:
        question: Business question to analyze
    """
    try:
        # Initialize components
        sql_agent = get_sql_agent()
        story_generator = get_story_generator()
        chart_generator = get_chart_generator()
        
        # Generate and execute SQL query
        with st.spinner("🔍 Generating SQL query..."):
            query_result = sql_agent.generate_sql(question)
        
        if not query_result.success:
            st.error(f"❌ SQL generation failed: {query_result.error}")
            return
        
        # Get column names from query result or generate them
        if query_result.columns:
            query_columns = query_result.columns
        else:
            # Fallback: generate generic column names based on actual data structure
            actual_column_count = len(query_result.data[0]) if query_result.data else 0
            query_columns = [f'column_{i+1}' for i in range(actual_column_count)]
        
        # Create story from results
        with st.spinner("📝 Generating insights..."):
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
        
        st.success("✅ Analysis completed successfully!")
        
    except Exception as e:
        logger.error(f"Analysis error: {e}")
        st.error(f"❌ Analysis failed: {str(e)}")

def display_analysis_results():
    """Display the analysis results in the view tab."""
    if not st.session_state.analysis_results:
        return
    
    results = st.session_state.analysis_results
    story = results['story']
    data = results['data']
    columns = results['columns']
    
    # Executive Summary
    st.markdown("### 📋 Executive Summary")
    st.info(story.executive_summary)
    
    # Key Insights
    st.markdown("### 💡 Key Insights")
    for insight in story.key_insights:
        st.markdown(f"• {insight}")
    
    # Visualization
    st.markdown("### 📊 Data Visualization")
    try:
        chart_generator = get_chart_generator()
        fig = chart_generator.auto_generate_chart(data, columns, results['question'])
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Visualization error: {e}")
    
    # Detailed Analysis
    st.markdown("### 🔍 Detailed Analysis")
    st.markdown(story.detailed_analysis)
    
    # Recommendations
    st.markdown("### 🎯 Recommendations")
    for i, rec in enumerate(story.recommendations, 1):
        st.markdown(f"{i}. {rec}")
    
    # Raw Data
    with st.expander("📋 Raw Data"):
        if data:
            df = pd.DataFrame(data, columns=columns)
            st.dataframe(df, use_container_width=True)
            st.markdown(f"**Query:** `{results['query']}`")
    
    # Follow-up Questions
    st.markdown("### ❓ Follow-up Questions")
    for question in story.follow_up_questions:
        if st.button(f"🔍 {question}", key=f"followup_{hash(question)}"):
            st.session_state.current_question = question
            st.rerun()

def display_sidebar():
    """Display sidebar with system information and controls."""
    with st.sidebar:
        st.markdown("### 🔧 System Status")
        
        # Database status
        db_status = check_database_connection()
        if db_status:
            st.markdown('<span class="status-success">✅ Database Connected</span>', unsafe_allow_html=True)
            
            # Display database info
            try:
                db = get_database()
                table_info = db.get_table_info()
                st.metric("Total Orders", f"{table_info['row_count']:,}")
                st.metric("Database Size", f"{len(table_info['schema'])} columns")
            except Exception as e:
                st.warning(f"Could not fetch database info: {e}")
        else:
            st.markdown('<span class="status-error">❌ Database Disconnected</span>', unsafe_allow_html=True)
            st.error("Please check your database connection")
        
        st.markdown("---")
        
        # Application info
        st.markdown("### 📊 Application Info")
        st.markdown("""
        **Features:**
        - Natural language queries
        - Multi-modal responses
        - Interactive visualizations
        - E-commerce insights
        
        **Data Period:** 2023
        **Customers:** 500 unique
        **Orders:** 10,000 total
        """)
        
        st.markdown("---")
        
        # Reset button
        if st.button("🔄 Reset Session"):
            st.session_state.messages = []
            st.session_state.current_question = ""
            st.session_state.analysis_results = None
            st.rerun()

def display_chat_tab():
    """Display the chat interface tab."""
    st.markdown('<div class="main-header">💬 Ask Your Business Question</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Ask questions about your e-commerce data in natural language</div>', unsafe_allow_html=True)
    
    # Check database connection
    if not check_database_connection():
        st.error("❌ Database connection failed. Please check your configuration.")
        return
    
    # Example questions
    with st.expander("💡 Example Questions", expanded=True):
        example_questions = [
            "What are our top-selling product categories?",
            "Show me monthly sales trends for 2023",
            "Which states generate the most revenue?",
            "What's the average order value by payment method?",
            "Which products have the highest return rates?",
            "Show me seasonal patterns in our sales data"
        ]
        
        cols = st.columns(2)
        for i, question in enumerate(example_questions):
            with cols[i % 2]:
                if st.button(f"📝 {question}", key=f"example_{i}", use_container_width=True):
                    st.session_state.current_question = question
                    st.rerun()
    
    # Chat input
    st.markdown("---")
    
    # Text input for questions
    question = st.text_area(
        "Your Question:",
        value=st.session_state.current_question,
        height=100,
        placeholder="Type your business question here... e.g., 'What are our top-selling products this year?'",
        key="question_input"
    )
    
    # Submit button
    col1, col2, col3 = st.columns([1, 1, 3])
    with col1:
        if st.button("🚀 Analyze", type="primary", use_container_width=True):
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
                    "content": "Analysis completed! Please visit the **View** tab to see the detailed results with charts and insights."
                })
                st.rerun()
            else:
                st.warning("Please enter a question first.")
    
    with col2:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.current_question = ""
            st.rerun()
    
    # Display chat history
    if st.session_state.messages:
        st.markdown("---")
        st.markdown("### 💬 Chat History")
        
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f"**You:** {message['content']}")
            else:
                st.markdown(f"**Assistant:** {message['content']}")
        
        # Clear history button
        if st.button("🗑️ Clear Chat History", type="secondary"):
            st.session_state.messages = []
            st.rerun()

def display_view_tab():
    """Display the analysis view tab."""
    st.markdown('<div class="main-header">📊 Analysis Results</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Rich insights and visualizations for your business questions</div>', unsafe_allow_html=True)
    
    # Check if there are analysis results
    if st.session_state.analysis_results:
        # Display analysis results
        display_analysis_results()
        return
    
    # Check if there's a current question
    if not st.session_state.current_question:
        st.info("👈 Please ask a question in the Chat tab to see analysis results here.")
        
        # Show sample data preview
        st.markdown("---")
        st.markdown("### 📋 Sample Data Preview")
        
        try:
            schema = get_schema()
            sample_data = schema.get_sample_data(10)
            
            if sample_data:
                df = pd.DataFrame(sample_data)
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("No sample data available")
        except Exception as e:
            st.error(f"Error loading sample data: {e}")
        
        # Show database schema
        st.markdown("---")
        st.markdown("### 🏗️ Database Schema")
        
        try:
            db = get_database()
            table_info = db.get_table_info()
            
            # Display schema information
            schema_df = pd.DataFrame(table_info['schema'], columns=['Column', 'Type', 'Null', 'Key', 'Default', 'Extra'])
            st.dataframe(schema_df, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error loading schema: {e}")
        
        return
    
    # Display current question
    st.markdown("### 🤔 Current Question")
    st.markdown(f"**Question:** {st.session_state.current_question}")
    
    # Analyze button for the view tab
    if st.button("🚀 Analyze This Question", type="primary", key="analyze_in_view"):
        perform_analysis(st.session_state.current_question)
        st.rerun()
    
    # Placeholder for analysis results
    st.markdown("---")
    st.markdown("### 🔄 Analysis Ready")
    
    st.info("""
    Click the **Analyze This Question** button above to generate:
    
    - **📊 Interactive Charts** - Dynamic visualizations using Plotly
    - **📈 Key Insights** - AI-generated business insights
    - **🔍 Detailed Analysis** - Comprehensive business analysis
    - **📋 Data Tables** - Relevant data supporting the analysis
    - **💡 Recommendations** - Actionable business recommendations
    - **❓ Follow-up Questions** - Related questions to explore
    
    All components are ready and integrated!
    """)
    
    # Show a simple query result as placeholder
    if st.button("🔍 Run Basic Query (Demo)"):
        try:
            db = get_database()
            # Simple demo query
            query = "SELECT product_category, COUNT(*) as order_count, SUM(quantity_ordered) as total_quantity FROM sales_table GROUP BY product_category ORDER BY order_count DESC"
            results = db.execute_query_df(query)
            
            st.markdown("### 📊 Sample Analysis Results")
            st.dataframe(results, use_container_width=True)
            
            # Simple chart
            st.bar_chart(results.set_index('product_category')['order_count'])
            
        except Exception as e:
            st.error(f"Error running demo query: {e}")

def main():
    """Main application function."""
    # Initialize session state
    initialize_session_state()
    
    # Display sidebar
    display_sidebar()
    
    # Main content area
    st.markdown('<div class="main-header">🛒 E-commerce Analytics</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Conversational Data Analytics for E-commerce Insights</div>', unsafe_allow_html=True)
    
    # Create tabs
    tab1, tab2 = st.tabs(["💬 Chat", "📊 View"])
    
    with tab1:
        display_chat_tab()
    
    with tab2:
        display_view_tab()
    
    # Footer
    st.markdown("---")
    st.markdown("*Powered by Streamlit, DuckDB, and AI*")

if __name__ == "__main__":
    main()