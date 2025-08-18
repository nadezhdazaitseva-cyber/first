# main.py
import json
from database import DatabaseManager
from data_handler import DataHandler
from data_processor import DataProcessor
import queries as sql_queries


def main():
    rooms = "https://raw.githubusercontent.com/nadezhdazaitseva-cyber/first/refs/heads/main/rooms.json"
    students = "https://raw.githubusercontent.com/nadezhdazaitseva-cyber/first/refs/heads/main/students.json"

    db_params = {
        'host': 'localhost',
        'database': 'postgres',
        'user': 'postgres',
        'password': '123',
        'port': '5432'
    }

    db_manager = DatabaseManager(db_params)
    try:
        db_manager.connect()
        data_handler = DataHandler(rooms, students)
        data_processor = DataProcessor(db_manager)

        # Initialize tables and triggers
        data_processor.initialize_tables()

        # Fetch and insert data
        rooms_data, students_data = data_handler.fetch_and_parse()
        data_processor.insert_data(rooms_data, students_data)

        # Run and handle queries
        queries_to_run = {
            'rooms_with_biggest_age_difference': sql_queries.rooms_with_biggest_age_difference,
            'rooms_with_smallest_avg_age': sql_queries.rooms_with_smallest_avg_age,
        }
        results = data_processor.run_queries(queries_to_run)

        # Handle output format
        format_choice = input("Enter output format (json or plain): ")
        if format_choice.lower() == 'json':
            with open('results.json', 'w') as f:
                json.dump(results, f, indent=2)
            print("Results saved to results.json")
        else:
            for query_name, result in results.items():
                print(f"\n--- Results for: {query_name} ---")
                print(result)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        db_manager.close()


if __name__ == '__main__':
    main()
