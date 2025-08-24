"""
query_executor.py.

This module provides a QueryExecutor to execute SQLfiles.
"""

import os
from work_with_DB.db_manager import DatabaseManager
from typing import List, Tuple, Any


class QueryExecutor:
    """High-level executor that runs SQL files from a given folder."""

    def __init__(self, db_manager: DatabaseManager, folder: str) -> None:
        """
        Initialize the DatabaseManager.

        :param db: Database manager instance
        :param folder: Path to folder with .sql files
        """
        self.db_manager = db_manager
        self.folder = folder

    def list_queries(self) -> List[str]:
        """
        List all .sql files with "SELECT" statment sorted by name.

        :return: filenames list
        """
        if not os.path.isdir(self.folder):
            raise ValueError(f"The folder '{self.folder}' doesn't exist.")
        return [f for f in sorted(os.listdir(self.folder))
                if f.endswith(".sql") and not f.startswith("insert_")]

    def execute_all(self) -> None:
        """Execute all SQL files in the folder(for DDL schema creation)."""
        if not os.path.isdir(self.folder):
            raise ValueError(f"The folder '{self.folder}' doesn't exist.")
        for file in self.list_queries():
            file_path = os.path.join(self.folder, file)
            with open(file_path, "r", encoding="utf-8") as f:
                query = f.read()
                try:
                    self.db_manager.execute(query)
                    print(f"📂 Executed {file}")
                except Exception as e:
                    print(f"Error executing DDL from {file}: {e}")
                    raise

    def execute_query(self, file_name: str) -> Tuple[List[str],
                                                     List[Tuple[Any, ...]]]:
        """
        Execute a single SQL file and return the results.

        Intended for DML (data manipulation).
        """
        file_path = os.path.join(self.folder, file_name)
        if not os.path.isfile(file_path):
            raise ValueError(f"""The file '{file_name}'
                             doesn't exist in folder '{self.folder}'.""")
        with open(file_path, "r", encoding="utf-8") as f:
            query = f.read()
            try:
                results = self.db_manager.execute(query)
                print(f"📂 Executed {file_name}")
                return results
            except Exception as e:
                print(f"Error executing DML from {file_name}: {e}")
                raise
