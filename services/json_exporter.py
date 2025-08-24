"""
JSON Exporter Module.

This module provides a concrete implementation of the BaseExporter class
for exporting query results to JSON files. It handles data transformation
from database rows to JSON format and writes to the specified file.
"""
import json
from typing import Any, List, Tuple

from services.base_exporter import BaseExporter


class JsonExporter(BaseExporter):
    """
    JSON file exporter implementation.

    This class extends the BaseExporter abstract class to provide specific
    functionality for exporting data to JSON format. It transforms database
    query results (columns and rows) into a list of dictionaries and writes
    them to a JSON file with proper formatting.

    Attributes:
        Inherits all attributes from BaseExporter.
    """

    def export(
            self,
            columns: List[str],
            rows: List[Tuple[Any, ...]],
            filename: str
                ) -> None:
        """Save rows and columns to a JSON file."""
        data = [dict(zip(columns, row)) for row in rows]
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Data successfully exported to {filename}")
