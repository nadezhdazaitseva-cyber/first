"""
Common Exporter Module.

This module provides a facade class that simplifies the process of exporting
data in various formats. It acts as a unified interface for multiple export
formats by delegating to specialized exporter classes.
"""

from typing import Any, Dict, List, Tuple

from services.base_exporter import BaseExporter
from services.json_exporter import JsonExporter
from services.xml_exporter import XmlExporter


class Exporter:
    """
    Facade that chooses a concrete exporter by format name.

    Supported: json, xml
    """

    def __init__(self) -> None:
        """
        Initialize the Exporter facade with supported format mappings.

        Sets up the internal mapping of format identifiers to their respective
        exporter instances. This allows for easy extension with new exporters
        by simply adding them to this mapping.
        """
        self._map: Dict[str, BaseExporter] = {
            "json": JsonExporter(),
            "xml": XmlExporter(),
        }

    def export(
            self,
            fmt: str,
            columns: List[str],
            rows: List[Tuple[Any, ...]],
            filename: str
                ) -> None:
        """
        Export rows/columns to a file in the requested format.

        :param fmt: "json" or "xml"
        :param columns: column names
        :param rows: list of tuples
        :param filename: output file path
        """
        fmt = fmt.lower()
        if fmt not in self._map:
            raise ValueError(f"Unsupported format: {fmt}")
        self._map[fmt].export(columns, rows, filename)
