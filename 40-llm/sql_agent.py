"""
LangChain SQL Agent for generating SQL queries from natural language.

This module provides SQL query generation capabilities using LangChain and OpenAI,
with comprehensive error handling and validation.
"""

import os
import logging
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
import sqlparse
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from langchain_community.llms import OpenAI
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage
from dotenv import load_dotenv
import sys
from pathlib import Path

# Add database module to path
sys.path.append(str(Path(__file__).parent.parent / "30-database"))
from connection import get_database
from schema import get_schema

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
DB_PATH = os.getenv('DUCKDB_PATH', '30-database/my_ecommerce_db.duckdb')
MAX_QUERY_ROWS = int(os.getenv('MAX_QUERY_ROWS', '10000'))
QUERY_TIMEOUT = int(os.getenv('QUERY_TIMEOUT', '30'))

if not OPENAI_API_KEY:
    logger.error("OPENAI_API_KEY not found in environment variables")
    raise ValueError("OPENAI_API_KEY is required")

@dataclass
class QueryResult:
    """Result of SQL query generation and execution."""
    success: bool
    query: Optional[str] = None
    data: Optional[List[tuple]] = None
    columns: Optional[List[str]] = None
    error: Optional[str] = None
    explanation: Optional[str] = None


class SQLQueryGenerator:
    """
    Generates SQL queries from natural language using LangChain and OpenAI.
    """

    def __init__(self):
        """Initialize the SQL query generator."""
        self.db = get_database()
        self.schema = get_schema()
        self.llm = self._initialize_llm()
        self.schema_context = self.schema.get_schema_context()

    def _initialize_llm(self) -> ChatOpenAI:
        """Initialize the OpenAI LLM."""
        try:
            return ChatOpenAI(
                model="gpt-4.1-nano-2025-04-14",
                temperature=0.8,
                openai_api_key=OPENAI_API_KEY,
                max_tokens=2000
            )
        except Exception as e:
            logger.error(f"Failed to initialize LLM: {e}")
            raise

    def _create_sql_prompt(self, question: str) -> List[Dict[str, str]]:
        """Create a structured prompt for SQL generation."""
        system_prompt = f"""
You are an expert SQL analyst for an e-commerce database. Your task is to generate accurate SQL queries based on natural language questions.

{self.schema_context}

IMPORTANT RULES:
1. ALWAYS use the table name 'sales_table' (no other tables exist)
2. Use exact column names as provided in the schema
3. Apply appropriate WHERE clauses, GROUP BY, ORDER BY as needed
4. Use LIMIT {MAX_QUERY_ROWS} for queries that might return many rows
5. For date queries, use DATE functions properly (dates are in YYYY-MM-DD format)
6. Return only the SQL query, no explanations or formatting
7. Ensure queries are syntactically correct for DuckDB
8. Use appropriate aggregation functions (SUM, COUNT, AVG, etc.)
9. For price calculations, multiply product_price by quantity_ordered
10. Consider both product_category and product_subcategory for detailed analysis

DUCKDB-SPECIFIC COMPATIBILITY:
- For percentiles, use QUANTILE_CONT(value, percentile) instead of APPROXIMATE_PERCENTILE
- For standard deviation, use STDDEV_SAMP() or STDDEV_POP()
- For variance, use VAR_SAMP() or VAR_POP()
- Window functions: ROW_NUMBER(), RANK(), DENSE_RANK() are supported
- For advanced analytics, prefer built-in statistical functions over complex subqueries

ADVANCED ANALYTICS PATTERNS:
- Percentile analysis: QUANTILE_CONT(order_value, 0.25) as q25, QUANTILE_CONT(order_value, 0.5) as median
- Standard deviation: STDDEV_SAMP(order_value) as std_dev
- Coefficient of variation: STDDEV_SAMP(value) / AVG(value) as cv
- Growth rates: Use LAG() window function for period-over-period calculations
- Top N analysis: Use ROW_NUMBER() OVER (ORDER BY metric DESC) for ranking

SAMPLE QUERIES:
- Sales trends: SELECT DATE_TRUNC('month', order_date) as month, SUM(product_price * quantity_ordered) as total_sales FROM sales_table GROUP BY month ORDER BY month;
- Top categories: SELECT product_category, COUNT(*) as orders, SUM(product_price * quantity_ordered) as revenue FROM sales_table GROUP BY product_category ORDER BY revenue DESC;
- State analysis: SELECT shipping_state, COUNT(*) as orders, AVG(product_price * quantity_ordered) as avg_order_value FROM sales_table GROUP BY shipping_state ORDER BY orders DESC;
"""

        user_prompt = f"""
Generate a SQL query for this question: {question}

Return only the SQL query, no additional text or formatting.
"""

        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

    def _validate_sql(self, query: str) -> bool:
        """Validate SQL query syntax."""
        try:
            # Parse the SQL query
            parsed = sqlparse.parse(query)
            if not parsed:
                return False

            # Check if it's a SELECT statement
            first_token = parsed[0].tokens[0]
            if first_token.ttype is sqlparse.tokens.Keyword and first_token.value.upper() != 'SELECT':
                logger.warning("Non-SELECT query detected")
                return False

            # Check for dangerous keywords
            dangerous_keywords = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'ALTER', 'CREATE', 'TRUNCATE']
            query_upper = query.upper()
            for keyword in dangerous_keywords:
                if keyword in query_upper:
                    logger.warning(f"Dangerous keyword detected: {keyword}")
                    return False

            return True
        except Exception as e:
            logger.error(f"SQL validation error: {e}")
            return False

    def _extract_column_names(self, query: str) -> List[str]:
        """Extract column names from SQL query."""
        try:
            import re

            # Clean the query
            query = query.strip()

            # Extract SELECT clause
            select_match = re.search(r'SELECT\s+(.*?)\s+FROM', query, re.IGNORECASE | re.DOTALL)
            if not select_match:
                return []

            select_clause = select_match.group(1).strip()

            # Handle different SELECT patterns
            columns = []

            # Split by comma, but handle functions
            parts = re.split(r',(?![^()]*\))', select_clause)

            for part in parts:
                part = part.strip()

                # Handle AS aliases
                if ' AS ' in part.upper():
                    alias_match = re.search(r' AS\s+(\w+)', part, re.IGNORECASE)
                    if alias_match:
                        columns.append(alias_match.group(1).lower())
                        continue

                # Handle common aggregations with better naming
                if 'COUNT(*)' in part.upper():
                    columns.append('count')
                elif 'COUNT(' in part.upper():
                    columns.append('count')
                elif 'SUM(' in part.upper():
                    # Try to extract what we're summing
                    if 'PRODUCT_PRICE' in part.upper():
                        columns.append('total_revenue')
                    elif 'QUANTITY' in part.upper():
                        columns.append('total_quantity')
                    else:
                        columns.append('total')
                elif 'AVG(' in part.upper():
                    # Try to extract what we're averaging
                    if 'PRODUCT_PRICE' in part.upper():
                        columns.append('avg_price')
                    elif 'QUANTITY' in part.upper():
                        columns.append('avg_quantity')
                    else:
                        columns.append('average')
                elif 'MAX(' in part.upper():
                    columns.append('maximum')
                elif 'MIN(' in part.upper():
                    columns.append('minimum')
                else:
                    # Extract column name
                    column_match = re.search(r'(\w+)$', part)
                    if column_match:
                        columns.append(column_match.group(1).lower())
                    else:
                        columns.append(f'column_{len(columns) + 1}')

            return columns

        except Exception as e:
            logger.error(f"Error extracting column names: {e}")
            return []

    def _generate_fallback_column_names(self, query: str, column_count: int) -> List[str]:
        """
        Generate fallback column names when extraction fails.

        Args:
            query: SQL query string
            column_count: Actual number of columns in the result

        Returns:
            List of descriptive column names
        """
        try:
            query_upper = query.upper()
            column_names = []

            # Analyze query to provide meaningful names
            for i in range(column_count):
                if i == 0:
                    # First column is often a grouping dimension
                    if 'GROUP BY' in query_upper:
                        if 'CATEGORY' in query_upper:
                            column_names.append('category')
                        elif 'STATE' in query_upper:
                            column_names.append('state')
                        elif 'DATE' in query_upper:
                            column_names.append('date')
                        elif 'PRODUCT' in query_upper:
                            column_names.append('product')
                        elif 'CUSTOMER' in query_upper:
                            column_names.append('customer')
                        else:
                            column_names.append('dimension')
                    else:
                        column_names.append('value')
                elif i == 1:
                    # Second column is often a measure
                    if 'COUNT(' in query_upper:
                        column_names.append('count')
                    elif 'SUM(' in query_upper:
                        column_names.append('total')
                    elif 'AVG(' in query_upper:
                        column_names.append('average')
                    elif 'STDDEV' in query_upper or 'STD(' in query_upper:
                        column_names.append('std_deviation')
                    elif 'PERCENTILE' in query_upper:
                        column_names.append('percentile')
                    else:
                        column_names.append('value')
                else:
                    # Additional columns
                    if 'STDDEV' in query_upper or 'STD(' in query_upper:
                        column_names.append(f'metric_{i}')
                    elif 'PERCENTILE' in query_upper:
                        column_names.append(f'percentile_{i}')
                    elif 'MIN(' in query_upper:
                        column_names.append('minimum')
                    elif 'MAX(' in query_upper:
                        column_names.append('maximum')
                    else:
                        column_names.append(f'column_{i + 1}')

            return column_names

        except Exception as e:
            logger.error(f"Error generating fallback column names: {e}")
            # Ultimate fallback
            return [f'column_{i + 1}' for i in range(column_count)]

    def generate_sql(self, question: str) -> QueryResult:
        """
        Generate SQL query from natural language question.

        Args:
            question: Natural language question

        Returns:
            QueryResult with generated query and execution results
        """
        try:
            # Create prompt
            messages = self._create_sql_prompt(question)

            # Generate SQL using LLM
            response = self.llm.invoke([
                SystemMessage(content=messages[0]["content"]),
                HumanMessage(content=messages[1]["content"])
            ])

            query = response.content.strip()

            # Clean the query (remove markdown formatting if present)
            if query.startswith('```sql'):
                query = query[6:]
            if query.endswith('```'):
                query = query[:-3]
            query = query.strip()

            # Validate the query
            if not self._validate_sql(query):
                return QueryResult(
                    success=False,
                    query=query,
                    error="Generated query failed validation"
                )

            # Execute the query
            try:
                data = self.db.execute_query(query)

                # Get actual column information from database execution
                # This is more reliable than parsing the SQL query
                if data and len(data) > 0:
                    # Infer column count from actual data
                    actual_column_count = len(data[0])

                    # Try to extract column names, but ensure count matches
                    extracted_names = self._extract_column_names(query)

                    # Create reliable column names
                    if len(extracted_names) == actual_column_count:
                        column_names = extracted_names
                    else:
                        # Fallback: create descriptive column names based on query analysis
                        column_names = self._generate_fallback_column_names(query, actual_column_count)
                else:
                    column_names = []

                return QueryResult(
                    success=True,
                    query=query,
                    data=data,
                    columns=column_names,
                    explanation=f"Query executed successfully, returned {len(data)} rows"
                )
            except Exception as e:
                logger.error(f"Query execution error: {e}")
                return QueryResult(
                    success=False,
                    query=query,
                    error=f"Query execution failed: {str(e)}"
                )

        except Exception as e:
            logger.error(f"SQL generation error: {e}")
            return QueryResult(
                success=False,
                error=f"SQL generation failed: {str(e)}"
            )

    def explain_query(self, query: str) -> str:
        """
        Generate explanation for a SQL query.

        Args:
            query: SQL query to explain

        Returns:
            Human-readable explanation of the query
        """
        try:
            prompt = f"""
Explain this SQL query in simple business terms:

{query}

Provide a clear, non-technical explanation of what this query does and what insights it provides.
"""

            response = self.llm.invoke([HumanMessage(content=prompt)])
            return response.content.strip()
        except Exception as e:
            logger.error(f"Query explanation error: {e}")
            return "Could not generate explanation for this query."

    def suggest_related_questions(self, question: str) -> List[str]:
        """
        Suggest related questions based on the current question.

        Args:
            question: Original question

        Returns:
            List of related questions
        """
        try:
            prompt = f"""
Based on this e-commerce analytics question: "{question}"

Suggest 5 related questions that would provide additional business insights.
Return only the questions, one per line, without numbering.
"""

            response = self.llm.invoke([HumanMessage(content=prompt)])
            suggestions = response.content.strip().split('\n')
            return [q.strip() for q in suggestions if q.strip()][:5]
        except Exception as e:
            logger.error(f"Question suggestion error: {e}")
            return []


# Global SQL agent instance
sql_agent = None

def get_sql_agent() -> SQLQueryGenerator:
    """
    Get the global SQL agent instance.

    Returns:
        SQLQueryGenerator: The global SQL agent instance
    """
    global sql_agent
    if sql_agent is None:
        sql_agent = SQLQueryGenerator()
    return sql_agent


def test_sql_agent():
    """Test the SQL agent functionality."""
    try:
        agent = get_sql_agent()

        # Test questions
        test_questions = [
            "What are the top 5 product categories by revenue?",
            "Show me monthly sales trends for 2023",
            "Which states have the highest average order value?"
        ]

        for question in test_questions:
            print(f"\n🔍 Testing: {question}")
            result = agent.generate_sql(question)

            if result.success:
                print(f"✅ Query: {result.query}")
                print(f"📊 Results: {len(result.data)} rows")
                if result.data:
                    print(f"Sample: {result.data[0]}")
            else:
                print(f"❌ Error: {result.error}")

        return True
    except Exception as e:
        print(f"❌ SQL Agent test failed: {e}")
        return False


if __name__ == "__main__":
    print("Testing SQL Agent...")
    test_sql_agent()
