# data_processor.py
from queries import create_rooms_table, create_students_table, create_func_and_trigger, insert_rooms, insert_students, \
    create_indexes
from .database import DatabaseManager


class DataProcessor:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def initialize_tables(self):
        self.db_manager.execute_query(create_rooms_table)
        self.db_manager.execute_query(create_students_table)
        self.db_manager.execute_query(create_func_and_trigger)
        self.db_manager.execute_query(create_indexes)
        self.db_manager.commit()
        print("Database schema initialized successfully.")

    def insert_data(self, rooms_data, students_data):
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
