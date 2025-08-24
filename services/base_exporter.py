"""
base_exporter.py.

This module provides an abstract BaseExporter class that serves as a foundation
for implementing concrete data exporter classes. The BaseExporter defines
a common interface for exporing data in various formats.

"""
from abc import ABC, abstractmethod
from typing import Any, List, Tuple


class BaseExporter(ABC):
    """Base interface for exporting tabular data to files."""

    @abstractmethod
    def export(
        self,
        columns: List[str],
        rows: List[Tuple[Any, ...]],
        filename: str
            ) -> None:
        """Save rows and columns to a file in a concrete format."""
        raise NotImplementedError
