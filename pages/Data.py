"""
Data page for E-commerce Analytics Application
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Add paths for custom modules
sys.path.append(str(Path(__file__).parent.parent / "30-database"))

try:
    from schema import get_schema
    from connection import get_database
except ImportError as e:
    st.error("Required modules not available. Please check your installation.")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="Data Overview",
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
    
    .info-box {
        background-color: #f8f9fa;
        padding: 1.2rem;
        border-radius: 8px;
        border-left: 4px solid #28a745;
        margin-bottom: 1rem;
    }
    
    .metric-container {
        text-align: center;
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1f77b4;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #666;
        margin-top: 0.2rem;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main data page function."""
    
    # Header
    st.markdown('<div class="main-title">Your Sales Data</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Understanding what information is available for analysis</div>', unsafe_allow_html=True)
    
    # Data metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-container">
            <div class="metric-value">10,000</div>
            <div class="metric-label">Total Orders</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-container">
            <div class="metric-value">500</div>
            <div class="metric-label">Unique Customers</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-container">
            <div class="metric-value">2023</div>
            <div class="metric-label">Data Period</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Available information
    st.markdown("### Available Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="info-box">
            <h4>Order & Product Data</h4>
            <ul>
                <li>Order dates and amounts</li>
                <li>Product categories and names</li>
                <li>Quantities purchased</li>
                <li>Payment methods used</li>
                <li>Pricing information</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-box">
            <h4>Customer & Financial Data</h4>
            <ul>
                <li>Customer locations (by state)</li>
                <li>Purchase history patterns</li>
                <li>Revenue by product/category</li>
                <li>Order values and trends</li>
                <li>Payment preferences</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Sample data preview
    st.markdown("### Sample Data Preview")
    
    try:
        schema = get_schema()
        sample_data = schema.get_sample_data(8)
        
        if sample_data:
            df = pd.DataFrame(sample_data)
            st.dataframe(df, use_container_width=True, height=300)
            st.caption("Sample of your sales data showing the information available for analysis.")
        else:
            st.warning("No sample data available")
    except Exception as e:
        st.error(f"Error loading sample data: {e}")
    
    # Example questions
    st.markdown("### Questions You Can Ask")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **Sales Performance**
        - "What are our top-selling product categories?"
        - "Show me monthly sales trends for 2023"
        - "Which products generate the most revenue?"
        - "What's our average order value?"
        """)
    
    with col2:
        st.markdown("""
        **Customer Insights**
        - "Which states are our best customers from?"
        - "How do customers prefer to pay?"
        - "Show me customer purchasing patterns"
        - "What's the geographic distribution of sales?"
        """)
    
    with col3:
        st.markdown("""
        **Product Analysis**
        - "Which product categories sell the most?"
        - "What are seasonal sales patterns?"
        - "Which products have highest profit margins?"
        - "Show me product performance trends"
        """)
    
    # Call to action
    st.markdown("""
    <div style="background-color: #e3f2fd; padding: 1.5rem; border-radius: 8px; text-align: center; margin-top: 2rem;">
        <h4>Ready to analyze your data?</h4>
        <p>Go to the <strong>Analysis</strong> page to start asking questions about your sales data.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()