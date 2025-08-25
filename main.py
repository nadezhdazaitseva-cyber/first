"""
The main module.

This script provides a command-line interface for:
  1) Running DDL scripts to initialize a PostgreSQL database schema
  2) Importing JSON datasets into corresponding tables
  3) Executing predefined DML queries interactively
  4) Exporting query results in JSON or XML format

Usage example for Linux/macOS:
--------------
python main.py \
    --data rooms=https://raw.githubusercontent.com/nadezhdazaitseva-cyber/first/refs/heads/main/rooms.json \
          students=https://raw.githubusercontent.com/nadezhdazaitseva-cyber/first/refs/heads/main/students.json \
    --format json
"""

import argparse
from typing import List, Tuple

from work_with_DB.db_manager import DatabaseManager
from loaders.json_loader import JsonLoader
from services.importer import Importer
from services.query_executor import QueryExecutor
from services.common_exporter import Exporter


def parse_data_args(pairs: List[str]) -> List[Tuple[str, str]]:
    """
    Parse ["table=path.json", ...] into list of (table, path).

    :raises ValueError: if a pair is malformed
    """
    parsed_pairs = []
    for pair in pairs:
        try:
            table, path = pair.split("=", 1)
            table = table.strip()
            path = path.strip()
            if not table or not path:
                raise ValueError(
                    f"""Invalid --data argument
                                 (expected table=path): {pair}"""
                )
            parsed_pairs.append((table, path))
        except ValueError:
            print(f"Invalid data pair: {pair}. Expected format: key=value")
    return parsed_pairs


def main() -> None:
    """
    Entry point.

      1) Run DDL from queries/DDL/
      2) Load any number of JSON files into corresponding tables
      3) Let user run DML queries from queries/DML/
      and choose export format each time
    """
    parser = argparse.ArgumentParser(
        description="""Generic PostgreSQL loader
                                     & query runner"""
    )
    parser.add_argument(
        "--data",
        nargs="+",
        required=True,
        metavar="table=path.json",    
        help="""Pairs "table=path.json"
        (rooms=parsed_files/rooms.json students=parsed_files/students.json)""",
    )
    parser.add_argument(
        "--format",
        choices=["json", "xml"],
        help=(
            "Optional default export format. "
            "If not provided, user will be asked interactively."
        ),
    )
    args = parser.parse_args()

    # Initialize db_manager
    with DatabaseManager() as db:

        try:
            # Step 1: Run DDL scripts to set up the database schema
            ddl = QueryExecutor(db, "queries/DDL")
            ddl.execute_all()

            # Step 2: Load JSON files into the database
            data_loader = JsonLoader()
            importer = Importer(db)

            for table, path in parse_data_args(args.data):
                records = data_loader.load(path)
                importer.import_data(table, records)
            print("Data import completed.")

            # Step 3: Interactive DML loop
            dml = QueryExecutor(db, "queries/DML")
            exporter = Exporter()

            queries = dml.list_queries()
            if not queries:
                print("No DML queries found in 'queries/DML/'. Exiting.")
                return

            print("\nAvailable queries:")
            for i, q in enumerate(queries, 1):
                print(f"{i}. {q}")

            while True:
                choice = (
                    input("\nChoose query number (or 'q' to quit): ")
                    .strip()
                    .lower()
                )
                # Check if the user wants to quit
                if choice == "q":
                    print("Exiting the program. \n👋 Bye!")
                    break

                # Check if the choice is a valid query number
                if not choice.isdigit() or not (
                    1 <= int(choice) <= len(queries)
                ):
                    print("❌ Invalid choice, try again.")
                    continue

                # Process the valid choice
                filename = queries[int(choice) - 1]
                cols, rows = dml.execute_query(filename)

                # Handle output format
                if args.format:
                    fmt = args.format
                else:
                    fmt = input("Export format (json/xml): ").strip().lower()

                if fmt not in ("json", "xml"):
                    print("❌ Unsupported format, try again.")
                    continue

                output = f"result_{filename}.{fmt}"
                exporter.export(fmt, cols, rows, output)
                print(f"✅ Saved to {output}")
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
