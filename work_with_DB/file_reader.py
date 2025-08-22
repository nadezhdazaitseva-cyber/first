# file_reader.py

import os
from typing import Dict, Any

def read_sql_file(file_path: str) -> str:
    """
    Reads the content of an SQL file and returns it as a string.
    
    Args:
        file_path (str): The path to the SQL file.
        
    Returns:
        str: The content of the SQL file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: SQL file not found at {file_path}")
        return ""

def load_all_sql_queries_from_dir(directory: str) -> Dict[str, str]:
    """
    Loads all SQL queries from .sql files in a specified directory.
    
    Args:
        directory (str): The path to the directory containing .sql files.
        
    Returns:
        Dict[str, str]: A dictionary where keys are filenames (without extension)
                        and values are the query strings.
    """
    queries = {}
    if not os.path.exists(directory):
        print(f"Directory not found: {directory}")
        return queries

    for filename in os.listdir(directory):
        if filename.endswith(".sql"):
            file_path = os.path.join(directory, filename)
            query_name = os.path.splitext(filename)[0]
            queries[query_name] = read_sql_file(file_path)
    return queries