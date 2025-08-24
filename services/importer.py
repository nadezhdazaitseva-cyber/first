"""
importer.py.

This module provides a concrete implementation of the DatabaseManager class
for importing data into a PostgreSQL database.
"""

from work_with_DB.db_manager import DatabaseManager
from typing import List, Dict


class Importer:
    """
    Class for importing data into the database.

    Attributes:
        db_manager (DatabaseManager): An instance of DatabaseManager
        to handle database operations.
    Methods:
        import_data(table: str, data: List[Dict]): Imports data into the
        specified table.
    """

    def __init__(self, db_manager: DatabaseManager):
        """Initialize the DatabaseManager."""
        self.db_manager = db_manager

    def get_table_columns(self, table: str) -> List[str]:
        """
        Retrieve the column names of the specified table.

        :param table: Name of the table to retrieve columns from
        :return: List of column names
        """
        query = """
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = %s
            ORDER BY ordinal_position;
        """
        column, rows = self.db_manager.execute(query, (table,))
        return [row[0] for row in rows]

    def import_data(self, table: str, data: List[Dict]) -> None:
        """
        Insert a list of dictionaries into the given table.

        :param table: Target table name
        :param records: List of dicts; keys should match table columns
        """
        if not data:
            print(f"⚠ No data provided for table '{table}'.")
            return

        table_columns = self.get_table_columns(table)
        if not table_columns:
            raise ValueError(f"Table '{table}' doesn't exist or has no column")
        for item in data:
            for key in item.keys():
                if key not in table_columns:
                    raise ValueError(f"""Column '{key}' does not exist
                                      in table '{table}'.""")
        normalized_data = []
        for row in data:
            new_row = {col: row[col] for col in table_columns if col in row}
            normalized_data.append(new_row)

        columns = normalized_data[0].keys()
        column_names = ', '.join(columns)
        placeholders = ', '.join(['%s'] * len(columns))
        insert_query = f"""
            INSERT INTO {table} ({column_names})
            VALUES ({placeholders})
            ON CONFLICT DO NOTHING;
        """

        values = [tuple(item[col] for col in columns) for item in data]

        try:
            with self.db_manager.conn.cursor() as cursor:
                cursor.executemany(insert_query, values)
            print(f"✅ Imported {len(normalized_data)} rows into '{table}'")
        except Exception as e:
            self.db_manager.conn.rollback()
            print(f"Error inserting data into '{table}': {e}")
            raise
