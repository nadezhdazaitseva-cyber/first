# main.py
import json
import os
from dotenv import load_dotenv
from work_with_DB.database import DatabaseManager
from work_with_DB.data_handler import DataHandler
from work_with_DB.data_processor import DataProcessor
import work_with_DB.file_reader as file_reader
import queries as sql_queries
import xml_generator
from typing import Dict, Any, List, Optional

# Load environment variables from .env file
load_dotenv()

def main() -> None:
    # URLs to fetch data from
    rooms = "https://raw.githubusercontent.com/nadezhdazaitseva-cyber/first/refs/heads/new_view/parsed_files/rooms.json"
    students = "https://raw.githubusercontent.com/nadezhdazaitseva-cyber/first/refs/heads/new_view/parsed_files/students.json"


    # Get database connection parameters from environment variables
    db_params = {
        'host': os.getenv('DB_HOST'),
        'database': os.getenv('DB_DATABASE'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'port': os.getenv('DB_PORT')
    }
    
    # Initialize db_manager to None before the try block to prevent the unbound error
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

       
        # Dynamically load all DML queries for the user interface
        all_user_queries: Dict[str, str] = file_reader.load_all_sql_queries_from_dir('queries_f/DML')
        
        # Create a numbered menu from the loaded queries
        all_queries: Dict[str, Dict[str, str]] = {}
        for i, query_name in enumerate(all_user_queries, start=1):
            all_queries[str(i)] = {
                'name': query_name.replace('_', ' ').title(),
                'query': all_user_queries.get(query_name, '')}

        # For user
        print("\n Select a query:")
        for key, value in all_queries.items():
            print(f"  {key}. {value['name']}")

        choice = ''
        while choice.lower() != 'q':
            choice = input("Enter the request number (or 'q' to quit): ")

            # Check if the user wants to quit
            if choice.lower() == 'q':
                print("Exiting the program.")
                break
            
            # Check if the choice is a valid query number
            if choice not in all_queries:
                print("Invalid request number. Please try again.")
                continue  # Skips the rest of the loop and re-prompts for a choice
            
            # Process the valid choice
            query_key = choice
            selected_queries = {
                all_queries[query_key]['name']: all_queries[query_key]['query']
            }
            results = data_processor.run_queries(selected_queries)

            # Handle output format
            format_choice = ''
            while format_choice.lower() not in ['j', 'x', 'p', 'q']:
                format_choice = input("Enter output format (j - json, x - xml, p - plain, or q - quit): ")

                if format_choice.lower() == 'j':
                    with open('results.json', 'w') as f:
                        json.dump(results, f, indent=2)
                    print("Results saved to results.json")
                elif format_choice.lower() == 'x':
                    xml_generator.save_xml(results)
                    print("Results saved to XML file.")
                elif format_choice.lower() == 'p':
                    for query_name, result in results.items():
                        print(f"\n--- Results for: {query_name} ---")
                        for el in result:
                            print(el) # Corrected print statement for tuples/lists
                elif format_choice.lower() == 'q':
                    print("Exiting output format selection.")
                    break
                else:
                    print("Invalid format choice. Please try again.")


    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        # Check if db_manager was created before trying to close it
        if 'db_manager' in locals() and db_manager:
            db_manager.close()


if __name__ == '__main__':
    main()
