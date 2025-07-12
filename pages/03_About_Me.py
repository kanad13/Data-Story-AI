"""
About Me page for the Data Story AI application.
"""

import streamlit as st

st.set_page_config(
    page_title="About Me - Data Story AI",
    page_icon="👨‍💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """Main function for the About Me page."""
    st.title("About Me")

    st.markdown("""
    ## Hi, I'm Kunal!

    I'm a passionate developer and data enthusiast who built 'Data Story AI' to bridge the gap between complex data and actionable business insights.

    With a background in software engineering and a deep interest in artificial intelligence, I believe that powerful analytics should be accessible to everyone, not just technical experts.

    ### Why I Built This Tool

    Throughout my career, I've seen countless organizations struggle with the same challenge: they have valuable data, but turning it into meaningful stories and actionable insights requires either technical expertise or long waits for analyst availability.

    I built 'Data Story AI' to democratize data analysis and enable anyone to have natural conversations with their data.
    """)

    st.header("Connect & Explore")

    st.markdown("""

    ### Personal Links
    - [My Portfolio Website](https://www.kunal-pathak.com)
    - [My Professional Profile](https://www.linkedin.com/in/kunal-pathak-profile/)
    - [My Open Source Contributions](https://github.com/kanad13)

    ### Project Resources
    - [View Source Code](https://github.com/kanad13/Data-Story-AI) for Data Story AI
    """)


    st.header("Acknowledgments")

    st.markdown("""
    This project wouldn't be possible without the incredible open-source community. Special thanks to:

    ### Core Technologies
    - **[Streamlit](https://streamlit.io/)** - For the beautiful and intuitive web framework
    - **[DuckDB](https://duckdb.org/)** - For the lightning-fast analytical database
    - **[LangChain](https://python.langchain.com/)** - For the powerful LLM orchestration framework
    - **[Plotly](https://plotly.com/python/)** - For the interactive visualization capabilities

    ### AI & Machine Learning
    - **[Pandas](https://pandas.pydata.org/)** - For data manipulation and analysis
    - **[NumPy](https://numpy.org/)** - For numerical computing foundations

    ### Development Tools
    - **[Python](https://python.org/)** - The language that makes it all possible
    - **[SQLParse](https://github.com/andialbrecht/sqlparse)** - For SQL query parsing and validation
    - **[Python-dotenv](https://github.com/theskumar/python-dotenv)** - For environment configuration management
    """)


if __name__ == "__main__":
    main()
