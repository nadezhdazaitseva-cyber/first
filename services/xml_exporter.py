"""
XML Exporter Module.

This module provides a concrete implementation of the BaseExporter class
for exporting query results to XML files. It transforms database query results
into a structured XML format with proper element hierarchy and encoding.
"""

import xml.etree.ElementTree as ET
from typing import Any, List, Tuple

from services.base_exporter import BaseExporter


class XmlExporter(BaseExporter):
    """
    Export query results to an XML file.

    This method transforms database query results into a structured XML format
    where each row becomes a <row> element with child elements for each column.
    The resulting XML document is written to a file with UTF-8 encoding and
    includes an XML declaration.
    """

    def export(
        self,
        columns: List[str],
        rows: List[Tuple[Any, ...]],
        filename: str
            ) -> None:
        """
        Export query results to an XML file.

        This method transforms database query results into a structured XML
        format where each row becomes a <row> element with child elements
        for each column. The resulting XML document is written to a file with
        UTF-8 encoding and includes an XML declaration.
        """
        root = ET.Element("results")

        for row in rows:
            row_element = ET.SubElement(root, "row")
            for col_name, value in zip(columns, row):
                child = ET.SubElement(row_element, col_name)
                child.text = "" if value is None else str(value)
            root.append(row_element)

        tree = ET.ElementTree(root)
        self._indent(root)
        tree.write(filename, encoding='utf-8', xml_declaration=True)
        print(f"Data successfully exported to {filename} in XML format.")

    def _indent(self, elem: ET.Element, level: int = 0) -> None:
        """
        Indent XML elements for pretty printing.

        This helper method recursively adds indentation to XML elements to
        improve readability when the XML is written to a file.
        """
        i = "\n" + level * "  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            for child in elem:
                self._indent(child, level + 1)
                if not child.tail or not child.tail.strip():
                    child.tail = i
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i
