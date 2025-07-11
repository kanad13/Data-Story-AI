"""
Database schema definitions and context for LLM integration.

This module provides comprehensive schema information, sample data, and business context
to help LLM agents understand the database structure and generate accurate SQL queries.
"""

from typing import Dict, List, Any
from dataclasses import dataclass
from connection import get_database

@dataclass
class ColumnInfo:
    """Information about a database column."""
    name: str
    type: str
    description: str
    sample_values: List[Any]
    business_context: str


class DatabaseSchema:
    """
    Provides comprehensive database schema information for LLM context.
    """
    
    def __init__(self):
        self.db = get_database()
        self._schema_info = self._build_schema_info()
    
    def _build_schema_info(self) -> Dict[str, ColumnInfo]:
        """Build comprehensive schema information."""
        return {
            'order_id': ColumnInfo(
                name='order_id',
                type='BIGINT',
                description='Unique identifier for each order',
                sample_values=[1, 2, 3, 4, 5],
                business_context='Primary key for orders, sequential numbering from 1 to 10,000'
            ),
            'customer_id': ColumnInfo(
                name='customer_id',
                type='BIGINT',
                description='Unique identifier for each customer',
                sample_values=[1, 50, 100, 200, 500],
                business_context='Customer ID ranges from 1 to 500, representing 500 unique customers'
            ),
            'order_date': ColumnInfo(
                name='order_date',
                type='TIMESTAMP_NS',
                description='Date and time when the order was placed',
                sample_values=['2023-01-15', '2023-06-20', '2023-09-10', '2023-12-05'],
                business_context='Orders span the entire year 2023 (Jan 1 - Dec 31), showing seasonal patterns'
            ),
            'product_name': ColumnInfo(
                name='product_name',
                type='VARCHAR',
                description='Full name of the product ordered',
                sample_values=['Apple iPhone 15 Pro Max', 'Samsung Galaxy S24 Ultra', 'Nike Air Force 1', 'Levi\'s 501 Jeans'],
                business_context='Real product names from major brands across all categories'
            ),
            'product_category': ColumnInfo(
                name='product_category',
                type='VARCHAR',
                description='Main product category',
                sample_values=['Electronics & Gadgets', 'Clothing & Apparel', 'Home & Furniture', 'Beauty & Personal Care'],
                business_context='8 main categories: Electronics & Gadgets, Clothing & Apparel, Home & Furniture, Books & Media, Beauty & Personal Care, Sports & Outdoors, Fashion Accessories, Toys & Games'
            ),
            'product_subcategory': ColumnInfo(
                name='product_subcategory',
                type='VARCHAR',
                description='Specific subcategory within the main category',
                sample_values=['Smartphones', 'Laptops', 'Men\'s Clothing', 'Skincare', 'Furniture'],
                business_context='Each category has 4 subcategories, allowing for detailed product classification'
            ),
            'quantity_ordered': ColumnInfo(
                name='quantity_ordered',
                type='BIGINT',
                description='Number of units ordered',
                sample_values=[1, 2, 3, 4, 5],
                business_context='Quantity ranges from 1 to 5 units per order, representing typical consumer purchasing patterns'
            ),
            'product_price': ColumnInfo(
                name='product_price',
                type='DOUBLE',
                description='Price per unit in USD',
                sample_values=[29.99, 199.99, 599.99, 1299.99],
                business_context='Prices vary by category: Electronics ($150-$3500), Clothing ($10-$400), Books ($4-$60), etc.'
            ),
            'payment_method': ColumnInfo(
                name='payment_method',
                type='VARCHAR',
                description='Method used to pay for the order',
                sample_values=['Credit Card', 'PayPal', 'Debit Card', 'Online Banking'],
                business_context='4 payment methods reflecting modern e-commerce preferences'
            ),
            'shipping_state': ColumnInfo(
                name='shipping_state',
                type='VARCHAR',
                description='US state where the order is shipped',
                sample_values=['California', 'Texas', 'New York', 'Florida', 'Illinois', 'Pennsylvania'],
                business_context='Orders ship to 6 major US states, representing key markets'
            ),
            'order_status': ColumnInfo(
                name='order_status',
                type='VARCHAR',
                description='Current status of the order',
                sample_values=['Placed', 'Processing', 'Shipped', 'Delivered', 'Cancelled', 'Returned'],
                business_context='6 order statuses representing the complete order lifecycle'
            )
        }
    
    def get_schema_context(self) -> str:
        """
        Get comprehensive schema context for LLM prompts.
        
        Returns:
            Formatted string with complete schema information
        """
        context = """
DATABASE SCHEMA CONTEXT FOR E-COMMERCE ANALYTICS

Table: sales_table
Description: Contains e-commerce order data with 10,000 orders from 500 unique customers across 2023.

COLUMNS:
"""
        
        for column_info in self._schema_info.values():
            context += f"""
- {column_info.name} ({column_info.type})
  Description: {column_info.description}
  Sample Values: {column_info.sample_values}
  Business Context: {column_info.business_context}
"""
        
        context += """
BUSINESS CONTEXT:
- Time Period: Full year 2023 (January 1 - December 31)
- Customer Base: 500 unique customers
- Order Volume: 10,000 total orders
- Product Range: 8 main categories with 4 subcategories each
- Geographic Coverage: 6 major US states
- Price Range: $1 - $10,000 depending on category

COMMON QUERY PATTERNS:
- Sales trends over time (monthly, quarterly, seasonal)
- Top-performing products and categories
- Customer behavior analysis
- Geographic sales distribution
- Payment method preferences
- Order status tracking
- Price analysis and profitability
- Inventory insights by category/subcategory

SAMPLE QUERIES:
1. Monthly sales trends: SELECT DATE_TRUNC('month', order_date) as month, SUM(product_price * quantity_ordered) as total_sales FROM sales_table GROUP BY month ORDER BY month;
2. Top categories: SELECT product_category, COUNT(*) as orders FROM sales_table GROUP BY product_category ORDER BY orders DESC;
3. Average order value by state: SELECT shipping_state, AVG(product_price * quantity_ordered) as avg_order_value FROM sales_table GROUP BY shipping_state ORDER BY avg_order_value DESC;
"""
        
        return context
    
    def get_column_info(self, column_name: str) -> ColumnInfo:
        """
        Get information about a specific column.
        
        Args:
            column_name: Name of the column
            
        Returns:
            ColumnInfo object with column details
        """
        return self._schema_info.get(column_name)
    
    def get_all_columns(self) -> List[str]:
        """
        Get all column names.
        
        Returns:
            List of column names
        """
        return list(self._schema_info.keys())
    
    def get_categories_and_subcategories(self) -> Dict[str, List[str]]:
        """
        Get mapping of categories to their subcategories.
        
        Returns:
            Dictionary mapping categories to subcategories
        """
        try:
            query = """
            SELECT DISTINCT product_category, product_subcategory 
            FROM sales_table 
            ORDER BY product_category, product_subcategory
            """
            results = self.db.execute_query(query)
            
            categories = {}
            for category, subcategory in results:
                if category not in categories:
                    categories[category] = []
                categories[category].append(subcategory)
            
            return categories
        except Exception as e:
            # Return default mapping if query fails
            return {
                'Electronics & Gadgets': ['Smartphones', 'Laptops', 'Headphones', 'Smartwatches'],
                'Clothing & Apparel': ['Men\'s Clothing', 'Women\'s Clothing', 'Shoes', 'Accessories'],
                'Home & Furniture': ['Furniture', 'Home Decor', 'Kitchen & Dining', 'Bedding & Bath'],
                'Books & Media': ['Books', 'E-books', 'Movies', 'Music'],
                'Beauty & Personal Care': ['Makeup', 'Skincare', 'Haircare', 'Fragrances'],
                'Sports & Outdoors': ['Fitness Equipment', 'Sports Apparel', 'Camping & Hiking', 'Cycling'],
                'Fashion Accessories': ['Jewelry', 'Watches', 'Bags & Luggage', 'Sunglasses'],
                'Toys & Games': ['Educational Toys', 'Action Figures', 'Board Games', 'Puzzles']
            }
    
    def get_sample_data(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get sample data from the database.
        
        Args:
            limit: Number of sample rows to return
            
        Returns:
            List of dictionaries containing sample data
        """
        try:
            query = f"SELECT * FROM sales_table LIMIT {limit}"
            results = self.db.execute_query(query)
            columns = self.get_all_columns()
            
            return [
                {columns[i]: row[i] for i in range(len(columns))}
                for row in results
            ]
        except Exception as e:
            return []
    
    def get_data_quality_info(self) -> Dict[str, Any]:
        """
        Get data quality information.
        
        Returns:
            Dictionary with data quality metrics
        """
        try:
            queries = {
                'total_rows': "SELECT COUNT(*) FROM sales_table",
                'unique_customers': "SELECT COUNT(DISTINCT customer_id) FROM sales_table",
                'unique_products': "SELECT COUNT(DISTINCT product_name) FROM sales_table",
                'date_range': "SELECT MIN(order_date), MAX(order_date) FROM sales_table",
                'null_values': "SELECT COUNT(*) FROM sales_table WHERE order_id IS NULL OR customer_id IS NULL"
            }
            
            quality_info = {}
            for key, query in queries.items():
                result = self.db.execute_query(query)
                quality_info[key] = result[0] if result else None
            
            return quality_info
        except Exception as e:
            return {'error': str(e)}


# Global schema instance
schema = DatabaseSchema()


def get_schema() -> DatabaseSchema:
    """
    Get the global schema instance.
    
    Returns:
        DatabaseSchema: The global schema instance
    """
    return schema


if __name__ == "__main__":
    # Test schema functionality
    print("Testing schema functionality...")
    
    schema_context = schema.get_schema_context()
    print("Schema context length:", len(schema_context))
    
    categories = schema.get_categories_and_subcategories()
    print("Categories:", list(categories.keys()))
    
    sample_data = schema.get_sample_data(3)
    print("Sample data rows:", len(sample_data))
    
    quality_info = schema.get_data_quality_info()
    print("Data quality info:", quality_info)