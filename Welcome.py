"""
Welcome page for Data Story AI Application
Based on README content and project positioning
"""

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Data Story AI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional layout
st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 3rem;
        padding-right: 3rem;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
        line-height: 1.2;
    }
    
    .hero-subtitle {
        font-size: 1.4rem;
        color: #666;
        text-align: center;
        margin-bottom: 3rem;
        font-weight: 400;
    }
    
    .problem-section {
        background-color: #ffebee;
        padding: 2rem;
        border-radius: 12px;
        border-left: 5px solid #e91e63;
        margin-bottom: 2rem;
    }
    
    .solution-section {
        background-color: #e8f5e8;
        padding: 2rem;
        border-radius: 12px;
        border-left: 5px solid #4caf50;
        margin-bottom: 2rem;
    }
    
    .feature-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        border: 1px solid #e9ecef;
        transition: transform 0.2s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 1rem;
    }
    
    .feature-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #333;
        margin-bottom: 0.5rem;
    }
    
    .feature-text {
        color: #666;
        line-height: 1.6;
    }
    
    .cta-section {
        background-color: #e3f2fd;
        padding: 2.5rem;
        border-radius: 12px;
        text-align: center;
        margin-top: 3rem;
    }
    
    .cta-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1976d2;
        margin-bottom: 1rem;
    }
    
    .nav-button {
        display: inline-block;
        padding: 12px 24px;
        margin: 8px;
        background-color: #1f77b4;
        color: white;
        text-decoration: none;
        border-radius: 6px;
        font-weight: 600;
        transition: background-color 0.3s ease;
    }
    
    .nav-button:hover {
        background-color: #1565c0;
        color: white;
        text-decoration: none;
    }
    
    .stats-container {
        display: flex;
        justify-content: space-around;
        margin: 2rem 0;
    }
    
    .stat-item {
        text-align: center;
        padding: 1rem;
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 800;
        color: #1f77b4;
        display: block;
    }
    
    .stat-label {
        font-size: 1rem;
        color: #666;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main welcome page function."""
    
    # Hero Section
    st.markdown('<div class="hero-title">Data Story AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">From Static Reports to Dynamic Conversations</div>', unsafe_allow_html=True)
    
    # Live Demo Link
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; margin: 2rem 0;">
            <a href="https://data-story-ai.streamlit.app" target="_blank" 
               style="background-color: #ff6b6b; 
                      color: white; padding: 15px 30px; border-radius: 25px; 
                      text-decoration: none; font-weight: bold; font-size: 1.1rem;
                      box-shadow: 0 4px 15px rgba(238, 90, 82, 0.3);">
                🚀 Try Live Demo
            </a>
        </div>
        """, unsafe_allow_html=True)
    
    # Problem Statement
    st.markdown("""
    <div class="problem-section">
        <h3>❌ The Problem with Traditional Business Intelligence</h3>
        <p>Business decisions need <strong>context</strong>, not just charts. Traditional BI creates fundamental gaps between data and action:</p>
        <ul>
            <li><strong>Technical Barriers:</strong> Requires SQL knowledge and analyst expertise</li>
            <li><strong>Time Delays:</strong> Weeks between questions and actionable insights</li>
            <li><strong>Static Reports:</strong> Charts without context or business narrative</li>
            <li><strong>Limited Access:</strong> Bottlenecks through technical teams</li>
        </ul>
        <p>Raw data doesn't tell you <em>why</em> revenue dropped or <em>what</em> to do about customer churn.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Solution Statement
    st.markdown("""
    <div class="solution-section">
        <h3>✅ Data Story AI Solution</h3>
        <p><strong>Data Story AI changes this.</strong> Our AI-powered tool automatically generates complete data stories from plain English questions:</p>
        <ul>
            <li><strong>No SQL Required:</strong> Ask questions in natural language</li>
            <li><strong>Instant Results:</strong> 2-5 second response times for complex analytics</li>
            <li><strong>Complete Stories:</strong> Context, insights, and actionable recommendations</li>
            <li><strong>Interactive Experience:</strong> Follow-up questions and deeper exploration</li>
        </ul>
        <p>The AI handles the entire process: understanding your question, generating SQL queries, analyzing results, and crafting complete business narratives with visualizations.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # What Data Stories Are
    st.markdown("## What Are Data Stories?")
    st.markdown("""
    Data stories bridge the gap between raw information and business action by combining three essential elements:
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <div class="feature-title">Data</div>
            <div class="feature-text">The Facts<br/>Revenue = $2M</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📖</div>
            <div class="feature-title">Narrative</div>
            <div class="feature-text">The Context<br/>40% growth from mobile</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📈</div>
            <div class="feature-title">Visuals</div>
            <div class="feature-text">The Clarity<br/>Trend charts & breakdown</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    **Result:** Instead of showing "Sales = $2M," a data story explains "Sales hit $2M driven by 40% growth in mobile purchases, suggesting we should prioritize our mobile experience."
    """)
    
    # Key Features
    st.markdown("## What Data Story AI Does For You")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🗣️</div>
            <div class="feature-title">Natural Language Interface</div>
            <div class="feature-text">Ask business questions in plain English: "Which products drove Q4 growth?" No SQL or technical jargon required.</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <div class="feature-title">Complete Data Stories</div>
            <div class="feature-text">Get comprehensive business narratives with executive summaries, actionable insights, and strategic recommendations.</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🎨</div>
            <div class="feature-title">Rich Visualizations</div>
            <div class="feature-text">Interactive charts you can explore, plus process diagrams that explain business workflows and patterns.</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">⚡</div>
            <div class="feature-title">Instant Analytics</div>
            <div class="feature-text">2-5 second response times for complex business questions with real-time data processing and follow-up capabilities.</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Sample Questions
    st.markdown("## Sample Questions to Try")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **Revenue Analysis**
        - "What are our top revenue-generating product categories?"
        - "Show me monthly sales trends for 2023"
        - "Which states generate the most revenue?"
        """)
    
    with col2:
        st.markdown("""
        **Customer Insights**
        - "Show me seasonal trends in customer purchasing behavior"  
        - "Which payment methods have the highest average order values?"
        - "What's the geographic distribution of our customers?"
        """)
    
    with col3:
        st.markdown("""
        **Product Performance**
        - "Which products have the highest profit margins?"
        - "Show me product category performance trends"
        - "What are our fastest-growing product segments?"
        """)
    
    # Technology Overview
    st.markdown("## How It Works")
    st.markdown("""
    Data Story AI combines multiple AI components in a sophisticated pipeline:
    
    - **🧠 Large Language Models:** Transform natural language into SQL queries and business narratives
    - **🔗 LangChain Framework:** Orchestrates AI workflows with conversation memory and error handling  
    - **📊 DuckDB Analytics:** Lightning-fast columnar database processing millions of rows in seconds
    - **🎨 Interactive Visualizations:** Plotly charts and Mermaid diagrams for rich, explorable insights
    - **🖥️ Streamlit Interface:** Responsive web app with real-time updates and chat-based interaction
    """)
    
    # Call to Action
    st.markdown("""
    <div class="cta-section">
        <div class="cta-title">Ready to Transform Your Data Analysis?</div>
        <p>Explore the demo dataset and try the AI chatbot to see Data Story AI in action.</p>
        <div style="margin-top: 2rem;">
            <a href="./01_Demo_Dataset" class="nav-button">📊 Explore Demo Dataset</a>
            <a href="./02_AI_Chatbot" class="nav-button">🤖 Try AI Chatbot</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()