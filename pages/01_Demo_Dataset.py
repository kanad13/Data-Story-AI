"""
Demo Dataset page for the Data Story AI application.
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Add paths for custom modules
sys.path.append(str(Path(__file__).parent.parent / "30-database"))

try:
    from schema import get_schema
    from connection import test_connection
except ImportError:
    st.error("Required modules not available. Please check your installation.")
    st.stop()

st.set_page_config(
    page_title="Demo Dataset - Data Story AI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """Main function for the Demo Dataset page."""
    st.title("Demo Dataset Overview")
    st.markdown("This page provides an overview of the sample e-commerce dataset used in 'Data Story AI'.")

    st.info("""
    **A Playground for Data Exploration**
    
    To help you get started, I've included this synthetic e-commerce dataset. It's designed to be a realistic playground that showcases how 'Data Story AI' can turn business questions into clear insights. While you can explore this demo data, you can also connect the tool to your own data sources.
    """)

    st.header("Dataset at a Glance")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Orders", "10,000")
    col2.metric("Unique Customers", "500")
    col3.metric("Product Categories", "8")
    col4.metric("Data Span", "Full Year 2023")

    st.header("What's Inside the Data?")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Product Details")
        st.write("Includes 8 major categories like Electronics, Clothing, and Home Goods, along with pricing and order quantities.")
        
        st.subheader("Transaction Information")
        st.write("Contains order dates, payment methods (Credit Card, PayPal, etc.), and current order statuses.")

    with col2:
        st.subheader("Customer Geography")
        st.write("Covers a distribution of customers across several states, including California, Texas, and New York.")

        st.subheader("Sales Over Time")
        st.write("The dataset spans the full year of 2023, making it ideal for analyzing seasonal and monthly trends.")

    st.header("Sample Data Preview")
    try:
        if test_connection():
            schema = get_schema()
            sample_data = schema.get_sample_data(10)
            if sample_data:
                df = pd.DataFrame(sample_data)
                st.dataframe(df, use_container_width=True, hide_index=True)
                st.caption("A snapshot of 10 sample orders from the dataset.")
            else:
                st.warning("Could not load sample data.")
        else:
            st.error("Database connection failed. Please check your configuration.")
    except Exception as e:
        st.error(f"An error occurred while loading the sample data: {e}")

    with st.expander("View the Complete Data Schema"):
        st.markdown("""
        Here is the structure of the `sales_table` used in this demo:
        
        | Column             | Type    | Description                               |
        |--------------------|---------|-------------------------------------------|
        | `order_id`         | INTEGER | Unique identifier for each order          |
        | `customer_id`      | INTEGER | Unique identifier for each customer       |
        | `order_date`       | DATE    | Date the order was placed                 |
        | `product_name`     | VARCHAR | Name of the purchased product             |
        | `product_category` | VARCHAR | Category of the product                   |
        | `quantity_ordered` | INTEGER | Number of items ordered                   |
        | `product_price`    | DECIMAL | Price per unit of the product             |
        | `payment_method`   | VARCHAR | Method used for payment                   |
        | `shipping_state`   | VARCHAR | State where the order was shipped         |
        """, unsafe_allow_html=True)

    st.header("Ready to Analyze?")
    st.success("""
    Now that you have a feel for the data, it's time to see 'Data Story AI' in action.
    
    Navigate to the **AI Chatbot** to start asking questions about this demo dataset.
    """)

if __name__ == "__main__":
    main()