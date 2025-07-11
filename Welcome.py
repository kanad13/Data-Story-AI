"""
Welcome page for E-commerce Analytics Application
"""

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="E-commerce Analytics",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for compact, professional layout
st.markdown("""
<style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    
    .feature-box {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #1f77b4;
        margin-bottom: 1rem;
    }
    
    .feature-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #333;
        margin-bottom: 0.5rem;
    }
    
    .feature-text {
        color: #666;
        line-height: 1.5;
    }
    
    .cta-box {
        background-color: #e3f2fd;
        padding: 1.5rem;
        border-radius: 8px;
        text-align: center;
        margin-top: 2rem;
    }
    
    .step-number {
        display: inline-block;
        background-color: #1f77b4;
        color: white;
        width: 24px;
        height: 24px;
        border-radius: 50%;
        text-align: center;
        font-weight: bold;
        margin-right: 8px;
        font-size: 0.9rem;
        line-height: 24px;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main welcome page function."""
    
    # Header
    st.markdown('<div class="main-title">E-commerce Analytics</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Analyze your sales data using natural language questions</div>', unsafe_allow_html=True)
    
    # Quick overview
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        This application helps you analyze your e-commerce sales data by asking questions in plain English. 
        Get instant insights about your customers, products, and sales performance with AI-powered analysis.
        """)
    
    with col2:
        st.markdown("""
        **Dataset Overview**
        - 10,000 orders
        - 500 customers  
        - 2023 sales data
        """)
    
    # Features in compact layout
    st.markdown("### Key Capabilities")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-box">
            <div class="feature-title">Natural Language Queries</div>
            <div class="feature-text">Ask questions like "What are my top-selling products?" or "Which states generate the most revenue?"</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-box">
            <div class="feature-title">Interactive Visualizations</div>
            <div class="feature-text">Get dynamic charts and graphs that make your data patterns easy to understand.</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-box">
            <div class="feature-title">AI-Powered Insights</div>
            <div class="feature-text">Receive detailed analysis, key insights, and business recommendations based on your data.</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-box">
            <div class="feature-title">Actionable Results</div>
            <div class="feature-text">Get clear answers with specific recommendations for improving your business performance.</div>
        </div>
        """, unsafe_allow_html=True)
    
    # How to use
    st.markdown("### How to Get Started")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <span class="step-number">1</span> **Explore Your Data**
        
        Check the Data page to understand what information is available in your dataset.
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <span class="step-number">2</span> **Ask Questions**
        
        Go to Analysis page and type your business questions in plain English.
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <span class="step-number">3</span> **Get Insights**
        
        Review the AI-generated analysis, charts, and actionable recommendations.
        """, unsafe_allow_html=True)
    
    # Call to action
    st.markdown("""
    <div class="cta-box">
        <h4>Ready to analyze your data?</h4>
        <p>Use the navigation sidebar to explore your dataset or start asking questions.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()