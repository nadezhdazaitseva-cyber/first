
# data_handler.py
import json
from urllib.request import urlopen


class DataHandler:
    def __init__(self, rooms_url, students_url):
        self.rooms_url = rooms_url
        self.students_url = students_url

    def fetch_and_parse(self):
        try:
            with urlopen(self.rooms_url) as rooms_response:
                rooms_data = json.load(rooms_response)
                print("Successfully parsed JSON rooms data.")
            with urlopen(self.students_url) as students_response:
                students_data = json.load(students_response)
                print("Successfully parsed JSON students data.")
            return rooms_data, students_data
        except Exception as e:
            print(f"Error fetching or parsing JSON data: {e}")
            raise
