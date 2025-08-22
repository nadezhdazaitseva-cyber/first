# main.py
import json
from work_with_DB.database import DatabaseManager
from work_with_DB.data_handler import DataHandler
from work_with_DB.data_processor import DataProcessor
import queries as sql_queries
import xml_generator

def main():
    rooms = "https://raw.githubusercontent.com/nadezhdazaitseva-cyber/first/refs/heads/main/rooms.json"
    students = "https://raw.githubusercontent.com/nadezhdazaitseva-cyber/first/refs/heads/main/students.json"

    # Default database connection parameters
    db_params = {
        'host': 'localhost',
        'database': 'postgres',
        'user': 'postgres',
        'password': '123',
        'port': '5432'
    }
    print('''We are going to work with the PostgreSQL database.
Do you want to use the default connection parameters [y - YES, n - NO]?
If not[n], you can enter your own parameters.''')
    
    input_db_params = input().strip().lower()

    if input_db_params == 'y':
        print("Using default connection parameters.")
        db_manager = DatabaseManager(db_params)
    elif input_db_params == 'n':
        db_params['host'] = input("Input host:").strip().lower()
        db_params['database'] = input("Input database name:").strip().lower()
        db_params['user'] = input("Input user name:").strip().lower()
        db_params['password'] = input("Input password:").strip() 
        db_params['port'] = input("Input port:").strip().lower()
        db_manager = DatabaseManager(db_params)
    else:
        print("Incorrect input. Using default connection parameters.")
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

        all_queries = {
            '1': {'name': 'Rooms with biggest age difference', 'query': sql_queries.rooms_with_biggest_age_difference},
            '2': {'name': 'Rooms with smallest avg age', 'query': sql_queries.rooms_with_smallest_avg_age},
            '3': {'name': 'List of rooms and students count', 'query': sql_queries.list_of_rooms_students},
            '4': {'name': 'Rooms with different gender students',
                  'query': sql_queries.rooms_with_different_gender_students}
        }

        # For user
        print("\n Select a query:")
        for key, value in all_queries.items():
            print(f"  {key}. {value['name']}")

        choice = input("Enter the request number : ")

        selected_queries = {}
        if choice in all_queries:
            query_key = choice
            selected_queries[all_queries[query_key]['name']] = all_queries[query_key]['query']
            results = data_processor.run_queries(selected_queries)

            # Handle output format
            format_choice = input("Enter output format (j - json, x - xml или p - plain): ")
            if format_choice.lower() == 'j':
                with open('results.json', 'w') as f:
                    json.dump(results, f, indent=2)
                    print("Results saved to results.json")
            elif format_choice.lower() == 'x':
                xml_generator.save_xml(results)
            else:
                for query_name, result in results.items():
                    print(f"\n--- Results for: {query_name} ---")
                    [print(*el) for el in result]
        else:
            print("Incorrect number. No request will be executed.")


    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        db_manager.close()


if __name__ == '__main__':
    main()
