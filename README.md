# Poly-Base: E-commerce Analytics with AI Agent

A conversational data analytics tool using Streamlit that allows users to ask business questions about e-commerce data and receive rich, multi-modal insights combining text explanations, process diagrams, and interactive visualizations.

## Project Structure

```
poly-base/
├── main.py                    # Main Streamlit application
├── 10-agent/                  # Agent instruction and workflow files
│   ├── 01-task-for-agent.md
│   ├── 02-instructions-for-agent.md
│   ├── 03-task-state-tracker.md
│   └── 04-response_guidelines.md
├── 20-config/                 # Configuration and data generation
│   └── 01-data_generator.py
├── 30-database/              # Database files and utilities
│   ├── connection.py          # DuckDB connection utilities
│   ├── schema.py             # Schema definitions for LLM context
│   └── my_ecommerce_db.duckdb # Pre-generated database
├── 40-llm/                   # LLM integration components
│   ├── sql_agent.py          # LangChain SQL agent configuration
│   └── story_generator.py    # OpenAI story generation logic
├── 50-visualization/         # Visualization components
│   ├── plotly_charts.py      # Data visualization components
│   └── mermaid_diagrams.py   # Process diagram utilities
├── .env                      # Environment variables (local)
├── .gitignore               # Git ignore patterns
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Setup Instructions

### 1. Environment Setup

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration

1. Copy `.env` and add your OpenAI API key:

```bash
cp .env .env.local
# Edit .env.local and add your actual OpenAI API key
```

### 3. Generate Database

```bash
# Generate the e-commerce database
cd 20-config
python 01-data_generator.py
```

This will create `30-database/my_ecommerce_db.duckdb` with 10,000 synthetic e-commerce orders.

### 4. Run the Application

```bash
# From the root directory
streamlit run main.py
```

## Features

- **Natural Language Queries**: Ask business questions in plain English
- **Multi-modal Responses**: Get text insights, charts, and process diagrams
- **E-commerce Analytics**: Analyze sales trends, customer behavior, and product performance
- **AI-Powered SQL Generation**: Automatic query generation from natural language
- **Interactive Visualizations**: Dynamic charts and graphs using Plotly
- **Process Diagrams**: Conceptual visualizations using Mermaid

## Usage

1. Navigate to the Chat tab
2. Ask a business question (e.g., "What are our top-selling product categories?")
3. View rich analysis results in the View tab

## Development Status

This project is currently in the planning and setup phase. The agent instruction files contain comprehensive development plans and workflows for building the complete application.

## License

MIT License (or specify your preferred license)
