"""
Database connection utilities for DuckDB.

This module provides connection management, query execution, and error handling
for the DuckDB database used in the e-commerce analytics application.
"""

import os
import logging
import duckdb
from typing import Optional, List, Dict, Any, Union
from contextlib import contextmanager
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database configuration - Use absolute path to avoid directory issues
def get_default_db_path():
    """Get the default database path relative to the project root."""
    # Get the project root directory (parent of 30-database)
    current_dir = Path(__file__).parent  # 30-database directory
    project_root = current_dir.parent    # project root directory
    return str(project_root / "30-database" / "my_ecommerce_db.duckdb")

DB_PATH = os.getenv('DUCKDB_PATH', get_default_db_path())
MAX_QUERY_ROWS = int(os.getenv('MAX_QUERY_ROWS', '10000'))
QUERY_TIMEOUT = int(os.getenv('QUERY_TIMEOUT', '30'))


class DatabaseConnection:
    """
    Manages DuckDB database connections with proper error handling and resource management.
    """
    
    def __init__(self, db_path: str = DB_PATH):
        """
        Initialize database connection.
        
        Args:
            db_path: Path to the DuckDB database file
        """
        self.db_path = db_path
        self._connection = None
        self._validate_database_path()
    
    def _validate_database_path(self) -> None:
        """Validate that database file exists and is accessible."""
        if not Path(self.db_path).exists():
            raise FileNotFoundError(f"Database file not found: {self.db_path}")
        
        if not Path(self.db_path).is_file():
            raise ValueError(f"Database path is not a file: {self.db_path}")
    
    @contextmanager
    def get_connection(self):
        """
        Context manager for database connections.
        
        Yields:
            duckdb.DuckDBPyConnection: Database connection object
        """
        try:
            connection = duckdb.connect(database=self.db_path, read_only=True)
            yield connection
        except Exception as e:
            logger.error(f"Database connection error: {e}")
            raise
        finally:
            if connection:
                connection.close()
    
    def execute_query(self, query: str, params: Optional[Dict[str, Any]] = None) -> List[tuple]:
        """
        Execute a SQL query and return results.
        
        Args:
            query: SQL query string
            params: Optional parameters for the query
            
        Returns:
            List of tuples containing query results
            
        Raises:
            Exception: If query execution fails
        """
        try:
            with self.get_connection() as conn:
                if params:
                    result = conn.execute(query, params).fetchall()
                else:
                    result = conn.execute(query).fetchall()
                
                # Apply row limit
                if len(result) > MAX_QUERY_ROWS:
                    logger.warning(f"Query returned {len(result)} rows, truncating to {MAX_QUERY_ROWS}")
                    result = result[:MAX_QUERY_ROWS]
                
                return result
        except Exception as e:
            logger.error(f"Query execution error: {e}")
            raise
    
    def execute_query_df(self, query: str, params: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
        """
        Execute a SQL query and return results as a pandas DataFrame.
        
        Args:
            query: SQL query string
            params: Optional parameters for the query
            
        Returns:
            pandas DataFrame containing query results
        """
        try:
            with self.get_connection() as conn:
                if params:
                    result = conn.execute(query, params).df()
                else:
                    result = conn.execute(query).df()
                
                # Apply row limit
                if len(result) > MAX_QUERY_ROWS:
                    logger.warning(f"Query returned {len(result)} rows, truncating to {MAX_QUERY_ROWS}")
                    result = result.head(MAX_QUERY_ROWS)
                
                return result
        except Exception as e:
            logger.error(f"Query execution error: {e}")
            raise
    
    def get_table_info(self, table_name: str = 'sales_table') -> Dict[str, Any]:
        """
        Get information about a table including schema and sample data.
        
        Args:
            table_name: Name of the table to inspect
            
        Returns:
            Dictionary containing table information
        """
        try:
            with self.get_connection() as conn:
                # Get table schema
                schema = conn.execute(f"DESCRIBE {table_name}").fetchall()
                
                # Get row count
                row_count = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
                
                # Get sample data
                sample_data = conn.execute(f"SELECT * FROM {table_name} LIMIT 5").fetchall()
                
                return {
                    'table_name': table_name,
                    'schema': schema,
                    'row_count': row_count,
                    'sample_data': sample_data
                }
        except Exception as e:
            logger.error(f"Error getting table info: {e}")
            raise
    
    def validate_connection(self) -> bool:
        """
        Validate database connection and basic functionality.
        
        Returns:
            True if connection is valid, False otherwise
        """
        try:
            with self.get_connection() as conn:
                # Test basic query
                result = conn.execute("SELECT 1").fetchone()
                return result == (1,)
        except Exception as e:
            logger.error(f"Connection validation failed: {e}")
            return False
    
    def get_table_columns(self, table_name: str = 'sales_table') -> List[str]:
        """
        Get column names for a table.
        
        Args:
            table_name: Name of the table
            
        Returns:
            List of column names
        """
        try:
            with self.get_connection() as conn:
                schema = conn.execute(f"DESCRIBE {table_name}").fetchall()
                return [column[0] for column in schema]
        except Exception as e:
            logger.error(f"Error getting table columns: {e}")
            raise


# Global database instance
db = DatabaseConnection()


def get_database() -> DatabaseConnection:
    """
    Get the global database instance.
    
    Returns:
        DatabaseConnection: The global database connection instance
    """
    return db


def test_connection() -> bool:
    """
    Test database connection.
    
    Returns:
        True if connection successful, False otherwise
    """
    try:
        return db.validate_connection()
    except Exception as e:
        logger.error(f"Database connection test failed: {e}")
        return False


if __name__ == "__main__":
    # Test the database connection
    print("Testing database connection...")
    
    if test_connection():
        print("✅ Database connection successful!")
        
        # Get table info
        table_info = db.get_table_info()
        print(f"Table: {table_info['table_name']}")
        print(f"Rows: {table_info['row_count']}")
        print(f"Columns: {len(table_info['schema'])}")
        
        # Test query
        sample_query = "SELECT product_category, COUNT(*) as count FROM sales_table GROUP BY product_category LIMIT 5"
        results = db.execute_query(sample_query)
        print(f"Sample query results: {results}")
        
    else:
        print("❌ Database connection failed!")