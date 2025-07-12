"""
Welcome page for the Data Story AI application.
"""

import streamlit as st

st.set_page_config(
    page_title="Welcome to Data Story AI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """Main function for the Welcome page."""
    st.title("Welcome to 'Data Story AI'")

    st.markdown("""
    I built this application because I saw how often organizations struggle to bridge the gap between their data and their decisions. Business intelligence tools can generate charts, but they often lack the context and narrative needed to drive meaningful action.
    
    'Data Story AI' is my solution to this problem. It's designed to transform your raw data into clear, actionable narratives.
    """)

    st.header("What Are Data Stories?")
    st.markdown("""
    A data story isn't just a collection of charts; it's a bridge between information and action. It combines three key elements:
    - **Data:** The objective facts (e.g., "Revenue was $2M last quarter.")
    - **Narrative:** The essential context (e.g., "...which was driven by a 40% increase in mobile engagement.")
    - **Visuals:** The supporting clarity (e.g., trend charts and breakdowns that illustrate the point.)
    
    The result is a powerful insight: "Sales hit $2M, driven by 40% growth in mobile purchases, suggesting we should prioritize our mobile experience."
    """)

    st.header("How 'Data Story AI' Helps")
    st.markdown("""
    Traditionally, creating data stories requires manual work from skilled analysts, which can be slow and create bottlenecks. I designed 'Data Story AI' to automate this process.
    
    This tool allows you to ask questions in plain English and receive a complete data story in seconds. It handles the complex work of writing SQL queries, analyzing the results, and generating a narrative with visualizations, so you can focus on the insights.
    """)

    st.header("Key Features")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🗣️ Natural Language Interface")
        st.write("Ask questions naturally, without needing to know SQL or technical jargon.")
        
        st.subheader("📊 Complete Data Stories")
        st.write("Receive comprehensive narratives that include an executive summary, key insights, and actionable recommendations.")

    with col2:
        st.subheader("🎨 Rich Visualizations")
        st.write("Instantly generate interactive charts and diagrams that help clarify the story behind the data.")

        st.subheader("⚡ Instant Analytics")
        st.write("Get answers in seconds, allowing you to explore data and ask follow-up questions in real time.")

    st.header("Get Started")
    st.success("""
    To see how it works, you can start by exploring the **Demo Dataset**. This is a sample dataset I've included so you can get a feel for the tool's capabilities.
    
    Once you're ready, head over to the **AI Chatbot** to analyze the demo data or connect to your own data source.
    """)

if __name__ == "__main__":
    main()