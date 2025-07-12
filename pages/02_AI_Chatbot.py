"""
AI Chatbot page for the Data Story AI application.
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Add paths for custom modules
sys.path.append(str(Path(__file__).parent.parent / "30-database"))
sys.path.append(str(Path(__file__).parent.parent / "40-llm"))
sys.path.append(str(Path(__file__).parent.parent / "50-visualization"))

try:
    from connection import test_connection
    from sql_agent import get_sql_agent
    from story_generator import get_story_generator
    from plotly_charts import get_chart_generator
except ImportError:
    st.error("Required modules not available. Please check your installation.")
    st.stop()

st.set_page_config(
    page_title="AI Chatbot - Data Story AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

def initialize_session_state():
    """Initializes session state variables."""
    if 'current_question' not in st.session_state:
        st.session_state.current_question = ""
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None

def perform_analysis(question: str):
    """Performs analysis of a business question."""
    try:
        sql_agent = get_sql_agent()
        story_generator = get_story_generator()

        with st.spinner("🔍 Analyzing your question..."):
            query_result = sql_agent.generate_sql(question)

        if not query_result.success:
            st.error(f"Analysis failed: {query_result.error}")
            return False

        with st.spinner("📖 Generating your data story..."):
            story = story_generator.generate_story(
                question,
                query_result.query,
                query_result.data,
                query_result.columns
            )

        st.session_state.analysis_results = {
            'question': question,
            'query': query_result.query,
            'data': query_result.data,
            'columns': query_result.columns,
            'story': story
        }
        return True

    except Exception as e:
        st.error(f"An error occurred during analysis: {e}")
        return False

def display_analysis_results():
    """Displays the analysis results in a structured format."""
    if not st.session_state.analysis_results:
        return

    results = st.session_state.analysis_results
    story = results['story']
    data = results['data']
    columns = results['columns']

    st.header(f"Data Story for: "f"'{results['question']}'")
    st.info(f"**Executive Summary:** {story.executive_summary}")

    st.subheader("📊 Data Visualization")
    try:
        chart_generator = get_chart_generator()
        fig = chart_generator.auto_generate_chart(data, columns, results['question'])
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.warning(f"Could not generate a visualization for this data. {e}")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("💡 Key Insights")
        for insight in story.key_insights:
            st.markdown(f"- {insight}")

    with col2:
        st.subheader("🎯 Recommendations")
        for rec in story.recommendations:
            st.markdown(f"- {rec}")

    with st.expander("Explore the Detailed Analysis, Raw Data, and SQL Query"):
        st.subheader("📝 Detailed Analysis")
        st.write(story.detailed_analysis)

        st.subheader("Raw Data Table")
        if data:
            # Handle column mismatch gracefully
            try:
                if len(data) > 0:
                    actual_cols = len(data[0])
                    if len(columns) != actual_cols:
                        if len(columns) < actual_cols:
                            columns = columns + [f'col_{i}' for i in range(len(columns), actual_cols)]
                        elif len(columns) > actual_cols:
                            columns = columns[:actual_cols]

                df = pd.DataFrame(data, columns=columns)
                st.dataframe(df, use_container_width=True)
            except Exception as e:
                st.warning(f"Could not display raw data table: {e}")
                st.text("Raw data:")
                for i, row in enumerate(data[:10]):  # Show first 10 rows as text
                    st.text(f"Row {i+1}: {row}")

        st.subheader("Generated SQL Query")
        st.code(results['query'], language='sql')



def main():
    """Main function for the AI Chatbot page."""
    initialize_session_state()

    st.title("'Data Story AI' Chatbot")
    st.markdown("Ask a question about the demo e-commerce data to generate an instant data story.")

    if not test_connection():
        st.error("Database connection failed. Please ensure your database is running and configured correctly.")
        return

    predefined_questions = [
        "Select a sample question",
        "Which states generate the most revenue?",
        "Calculate the standard deviation of order values by product category",
        "Show purchase frequency analysis: customers by number of orders placed",
        "Calculate conversion metrics: orders vs cancelled/returned orders by category",
        "Analyze payment method adoption trends over time",
        "Other (type your own question below)"
    ]

    selected_question = st.selectbox(
        "Start with a sample question or select 'Other' to ask your own:",
        predefined_questions,
        index=0,
        key="question_selector"
    )

    if selected_question == "Other (type your own question below)":
        current_question = st.text_input(
            "Enter your question here:",
            key="custom_question_input",
            placeholder="e.g., What are the most profitable products?"
        )
    elif selected_question != "Select a sample question":
        current_question = selected_question
    else:
        current_question = ""

    if st.button("Generate Data Story", disabled=not current_question, use_container_width=True):
        if current_question:
            st.session_state.current_question = current_question
            if perform_analysis(current_question):
                st.success("Your data story is ready!")
                # This rerun is to ensure the display function is called immediately after analysis
                st.rerun()
        else:
            st.warning("Please select or enter a question first.")

    if st.session_state.analysis_results:
        display_analysis_results()
    else:
        st.info("Your generated data story will appear here after you ask a question.")

if __name__ == "__main__":
    main()
