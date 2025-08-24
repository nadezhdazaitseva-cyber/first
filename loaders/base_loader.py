"""
base_loader.py.

This module provides an abstract BaseLoader class that serves as a foundation
for implementing concrete data loader classes. The BaseLoader defines a common
interface for loading data from various file formats and returning data.

"""

from abc import ABC, abstractmethod
from typing import List, Dict


class BaseLoader(ABC):
    """
    Abstract base class for data loaders.

    Defines the interface that all concrete data loader implementations
    must follow. Subclasses should implement the load method to handle specific
    file formats (JSON, XML, etc.) and return data in a standardized structure.
    """

    @abstractmethod
    def load(self, file_path: str) -> List[Dict]:
        """
        Load and parse data from a file into a structured format.

            :param file_path: the path to the file
            :return: list of dictionaries
        """
        pass
