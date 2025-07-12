"""
Demo Dataset page for Data Story AI Application
Explains the synthetic e-commerce data used for demonstration
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Add paths for custom modules
sys.path.append(str(Path(__file__).parent.parent / "30-database"))

try:
    from schema import get_schema
    from connection import get_database, test_connection
except ImportError as e:
    st.error("Required modules not available. Please check your installation.")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="Demo Dataset",
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
    
    .main-title {
        font-size: 2.8rem;
        font-weight: 700;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .subtitle {
        font-size: 1.3rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .info-section {
        background-color: #e3f2fd;
        padding: 2rem;
        border-radius: 12px;
        border-left: 5px solid #2196f3;
        margin-bottom: 2rem;
    }
    
    .metric-container {
        text-align: center;
        background-color: #f3e5f5;
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        border: 1px solid #e1bee7;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: #7b1fa2;
        display: block;
    }
    
    .metric-label {
        font-size: 1rem;
        color: #666;
        margin-top: 0.5rem;
        font-weight: 500;
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
    
    .feature-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #333;
        margin-bottom: 1rem;
    }
    
    .feature-text {
        color: #666;
        line-height: 1.6;
    }
    
    .sample-questions {
        background-color: #fff3e0;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 5px solid #ff9800;
    }
    
    .cta-section {
        background-color: #e8f5e8;
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        margin-top: 2rem;
    }
    
    .nav-button {
        display: inline-block;
        padding: 12px 24px;
        margin: 8px;
        background-color: #4caf50;
        color: white;
        text-decoration: none;
        border-radius: 6px;
        font-weight: 600;
        transition: background-color 0.3s ease;
    }
    
    .nav-button:hover {
        background-color: #388e3c;
        color: white;
        text-decoration: none;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main demo dataset page function."""
    
    # Header
    st.markdown('<div class="main-title">Demo Dataset Overview</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Understanding the synthetic e-commerce data powering our AI demonstrations</div>', unsafe_allow_html=True)
    
    # Dataset Context
    st.markdown("""
    <div class="info-section">
        <h3>🎯 Why This Dataset?</h3>
        <p>We use a carefully crafted synthetic e-commerce dataset that represents real-world business scenarios without exposing sensitive information. This dataset demonstrates how Data Story AI can transform complex business questions into actionable insights across various dimensions of e-commerce analytics.</p>
        <p><strong>Key Benefits:</strong></p>
        <ul>
            <li><strong>Realistic Patterns:</strong> Reflects actual e-commerce trends and seasonality</li>
            <li><strong>Complete Coverage:</strong> Includes all major business dimensions (products, customers, time, geography)</li>
            <li><strong>Rich Relationships:</strong> Complex data relationships that showcase AI capabilities</li>
            <li><strong>Privacy Safe:</strong> No real customer or business data involved</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Dataset Metrics
    st.markdown("## Dataset at a Glance")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-container">
            <span class="metric-value">10,000</span>
            <div class="metric-label">Total Orders</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-container">
            <span class="metric-value">500</span>
            <div class="metric-label">Unique Customers</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-container">
            <span class="metric-value">8</span>
            <div class="metric-label">Product Categories</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-container">
            <span class="metric-value">2023</span>
            <div class="metric-label">Full Year Data</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Business Context
    st.markdown("## Business Context & Scenarios")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">📱 Product Categories</div>
            <div class="feature-text">
                <strong>8 Major Categories:</strong><br/>
                • Electronics & Gadgets<br/>
                • Clothing & Apparel<br/>
                • Home & Furniture<br/>
                • Books & Media<br/>
                • Beauty & Personal Care<br/>
                • Sports & Outdoors<br/>
                • Fashion Accessories<br/>
                • Toys & Games
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">💳 Transaction Details</div>
            <div class="feature-text">
                <strong>Complete Order Information:</strong><br/>
                • Order dates and amounts<br/>
                • Product pricing and quantities<br/>
                • Payment methods (Credit Card, PayPal, Debit Card, Online Banking)<br/>
                • Order status tracking<br/>
                • Revenue and profitability data
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">🌍 Geographic Distribution</div>
            <div class="feature-text">
                <strong>Multi-State Coverage:</strong><br/>
                • California, Texas, New York<br/>
                • Florida, Illinois, Pennsylvania<br/>
                • Regional sales patterns<br/>
                • Geographic performance analysis<br/>
                • State-level customer insights
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">📈 Temporal Patterns</div>
            <div class="feature-text">
                <strong>Full Year 2023 Coverage:</strong><br/>
                • Seasonal trends and patterns<br/>
                • Monthly and quarterly analysis<br/>
                • Holiday shopping impacts<br/>
                • Growth trends over time<br/>
                • Business cycle insights
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Sample Data Preview
    st.markdown("## Sample Data Preview")
    
    try:
        # Test database connection
        if test_connection():
            schema = get_schema()
            sample_data = schema.get_sample_data(10)
            
            if sample_data:
                df = pd.DataFrame(sample_data)
                
                # Display sample with better formatting
                st.dataframe(
                    df, 
                    use_container_width=True, 
                    height=400,
                    hide_index=True
                )
                st.caption("Sample of 10 orders showing the structure and variety of data available for analysis.")
                
                # Data schema information
                with st.expander("📋 View Complete Data Schema"):
                    st.markdown("""
                    **Table: sales_table**
                    
                    | Column | Type | Description |
                    |--------|------|-------------|
                    | order_id | INTEGER | Unique identifier for each order |
                    | customer_id | INTEGER | Unique identifier for each customer |
                    | order_date | DATE | Date when the order was placed |
                    | product_name | VARCHAR | Full name of the purchased product |
                    | product_category | VARCHAR | Main category (e.g., Electronics & Gadgets) |
                    | product_subcategory | VARCHAR | Specific subcategory (e.g., Smartphones) |
                    | quantity_ordered | INTEGER | Number of items ordered |
                    | product_price | DECIMAL | Price per unit of the product |
                    | payment_method | VARCHAR | Method used for payment |
                    | shipping_state | VARCHAR | State where the order was shipped |
                    | order_status | VARCHAR | Current status of the order |
                    """)
            else:
                st.warning("No sample data available at the moment.")
        else:
            st.error("Unable to connect to the database. Please check the configuration.")
    except Exception as e:
        st.error(f"Error loading sample data: {e}")
    
    # Questions You Can Ask
    st.markdown("## Business Questions This Dataset Can Answer")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="sample-questions">
            <h4>💰 Revenue Analysis</h4>
            <ul>
                <li>"What are our top revenue-generating product categories?"</li>
                <li>"Show me monthly sales trends for 2023"</li>
                <li>"Which states generate the most revenue?"</li>
                <li>"What's our average order value?"</li>
                <li>"Which products have the highest profit margins?"</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="sample-questions">
            <h4>👥 Customer Insights</h4>
            <ul>
                <li>"How do customers prefer to pay?"</li>
                <li>"What's the geographic distribution of sales?"</li>
                <li>"Show me customer purchasing patterns"</li>
                <li>"Which states have the most loyal customers?"</li>
                <li>"What are peak shopping periods?"</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="sample-questions">
            <h4>📊 Product Performance</h4>
            <ul>
                <li>"Which product categories sell the most?"</li>
                <li>"What are seasonal sales patterns?"</li>
                <li>"Show me product performance trends"</li>
                <li>"Which items have highest quantities ordered?"</li>
                <li>"What are our fastest-growing segments?"</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Technical Details
    st.markdown("## Technical Implementation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🗄️ Database Technology**
        - **DuckDB**: High-performance analytical database
        - **Columnar Storage**: Optimized for analytical queries
        - **SQL Compatible**: Standard SQL syntax support
        - **Fast Aggregations**: Sub-second query responses
        """)
    
    with col2:
        st.markdown("""
        **🔧 Data Generation**
        - **Synthetic but Realistic**: Generated using statistical models
        - **Business Logic**: Follows real e-commerce patterns
        - **Quality Assured**: Validated for consistency and completeness
        - **Scalable Design**: Easy to generate larger datasets
        """)
    
    # Call to Action
    st.markdown("""
    <div class="cta-section">
        <h3>Ready to Explore the Data?</h3>
        <p>Now that you understand the dataset, try asking questions about it using our AI chatbot!</p>
        <div style="margin-top: 1.5rem;">
            <a href="./02_AI_Chatbot" class="nav-button">🤖 Try AI Chatbot</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()