# data_processor.py
from queries import insert_rooms, insert_students
from .database import DatabaseManager


class DataProcessor:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def initialize_tables(self, queries=None):
        if queries is None:
            print("No queries provided for initializing tables.")
            return

        for query_name, query in queries.items():
            try:
                self.db_manager.execute_query(query)
                print(f"Executed: {query_name}")
            except Exception as e:
                print(f"Error executing {query_name}: {e}")
        self.db_manager.commit()
        print("Database schema initialized successfully.")

    def insert_data(self, rooms_data, students_data):
        if self.db_manager.cursor is None:
            raise RuntimeError("Database cursor is not initialized. Did you call connect()?")

        room_tuples = [(room['id'], room['name']) for room in rooms_data]
        student_tuples = [(student['id'], student['birthday'], student['name'], student['room'], student['sex']) for student in students_data]

        self.db_manager.cursor.executemany(insert_rooms, room_tuples)
        self.db_manager.cursor.executemany(insert_students, student_tuples)
        self.db_manager.commit()
     #  print(f"Successfully inserted {len(rooms_data)} rooms.")
     #  print(f"Successfully inserted {len(student_tuples)} students.")

    def run_queries(self, queries_to_run):
        results = {}
        for query_name, query_string in queries_to_run.items():
            try:
                result = self.db_manager.execute_query(query_string)
                results[query_name] = result
                print(f"Query '{query_name}' executed successfully.")
            except Exception as e:
                print(f"Error executing query '{query_name}': {e}")
        return results