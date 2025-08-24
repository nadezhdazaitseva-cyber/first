# xml_exporter.py

import lxml.etree as et


def generate_xml(data):
    """
    Generates an XML document from a dictionary with query results.

    :param data: A dictionary where the key is the query name and the 
    value is — a list of tuples (results of an SQL query).
    :return: A byte string with a formatted XML document.
    """
    # Creating a root <results> element using lxml.etree.Element
    root = et.Element("results")

    # go through each query and its results in the dictionary
    for query_name, results_list in data.items():

        query_element = et.SubElement(root, query_name)

        # Iterating through each row (tuple) from the query results
        for row_tuple in results_list:
            #  Creating a <row> element for each row of data
            row_element = et.SubElement(query_element, "row")

            #  For each value in the tuple, create a <column> element
            for value in row_tuple:
                column_element = et.SubElement(row_element, "column")
                column_element.text = str(value)

    return et.tostring(
        root,
        pretty_print=True,
        xml_declaration=True,
        encoding='UTF-8'
    )


def save_xml(data, filename="results.xml"):
    try:
        xml_data = generate_xml(data)
        with open(filename, 'wb') as f:
            f.write(xml_data)
        print(f"Results saved to results.json{filename}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
