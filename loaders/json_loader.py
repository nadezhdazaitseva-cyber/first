"""
json_loader.py.

This module provides a concrete implementation of the BaseLoader class
for loading and parsing JSON files. It handles JSON file reading and
returns the data as structured Python objects.
"""

import json
import urllib.request
import urllib.error
from typing import List, Dict
from loaders.base_loader import BaseLoader


class JsonLoader(BaseLoader):
    """
    JSON file loader.

    This class extends the BaseLoader abstract class to provide specific
    functionality for loading and parsing JSON files. It reads JSON data
    from files and returns it as Python dictionaries and lists.
    """

    def load(self, file_path: str) -> List[Dict]:
        """
        Load and parse data from a JSON file.

        This method reads a JSON file from the specified path,
        parses its contents, and returns the data as Python objects.

        :param file_path: Path to the JSON file to be loaded
        :type file_path: str
        :return: Parsed JSON data as a list of dictionaries
        :rtype: List[Dict]
        :raises FileNotFoundError: If the specified JSON file does not exist
        """
        try:
            if file_path.startswith(('http://', 'https://')):
                # Load JSON from URL
                with urllib.request.urlopen(file_path) as response:
                    data = json.loads(response.read().decode())
            else:
                # Load JSON from local file system
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            if not isinstance(data, list):
                raise ValueError("JSON data must be a list of dictionaries.")
        except FileNotFoundError:
            raise FileNotFoundError(f"The JSON file wasn't found: {file_path}")
        except urllib.error.URLError as e:
            raise ValueError(f"""Failed to load JSON from URL: {file_path}.
                              Error: {e}""")
        except json.JSONDecodeError as e:
            raise ValueError(f"""Error decoding JSON from file: {file_path}.
                             Error: {e}""")
        return data
