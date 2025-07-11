"""
Database package for e-commerce analytics application.
"""

from .connection import get_database, test_connection, DatabaseConnection
from .schema import get_schema, DatabaseSchema

__all__ = [
    'get_database',
    'test_connection', 
    'DatabaseConnection',
    'get_schema',
    'DatabaseSchema'
]