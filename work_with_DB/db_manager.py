"""
db_manager.py.

This module provides a DatabaseManager class for
managing PostgreSQL database connections and executing SQL queries.
"""
import os
import psycopg2
from psycopg2.extensions import connection
from dotenv import load_dotenv
from typing import Optional, Tuple, List, Any


class DatabaseManager:
    """
    Low-level PostgreSQL connection manager.

    Manages connection, SQL query execution and transactions.
    Attributes:
        conn (connection): The database connection object.
        cursor: The database cursor object.
    Methods:
        execute(query: str, params: Optional[tuple] = None):
            Executes an SQL query with or without returning a result.
        close(): Closes the database connection.
    """

    def __init__(self) -> None:
        """Initialize the DatabaseManager."""
        load_dotenv()  # Load environment variables from .env file
        self.conn: connection = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_DATABASE'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            port=os.getenv('DB_PORT')
        )
        print("Connected to PostgreSQL database!")
        self.conn.autocommit = True  # Enable autocommit mode

    def __enter__(self) -> "DatabaseManager":
        """Enter the runtime context related to this object."""
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """Exit the runtime context and close the connection."""
        self.close()

    def execute(
            self,
            query: str,
            params: Optional[Tuple[Any, ...]] = None,
    ) -> Tuple[List[str], List[Tuple[Any, ...]]]:
        """
        Execute a SQL query. If it is a SELECT, returns (columns, rows).

        For non-SELECT queries, commits and returns ([], []).

        :param query: SQL query string
        :param params: optional parameters tuple
        :return: (list of column names, list of row tuples)
        """
        if self.conn.cursor is None:
            raise RuntimeError("Database cursor is not initialized.")

        with self.conn.cursor() as cur:
            cur.execute(query, params)

            if cur.description:  # If the query returns rows (e.g., SELECT)
                columns = [desc[0] for desc in cur.description]
                rows = cur.fetchall()
                return columns, rows

            return [], []

    def close(self):
        """Close the database connection."""
        if self.conn is not None:
            self.conn.close()
            print("Database connection closed.")
