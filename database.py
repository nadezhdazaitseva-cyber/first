# database.py
import psycopg2
from psycopg2 import sql


class DatabaseManager:
    def __init__(self, db_params):
        self.db_params = db_params
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(**self.db_params)
            self.cursor = self.conn.cursor()
            print("Connected to PostgreSQL database!")
        except psycopg2.Error as e:
            print(f"Database connection error: {e}")
            raise

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            print("Database connection closed.")

    def execute_query(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            if query.strip().lower().startswith(('select', 'with')):
                return self.cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Database error during query execution: {e}")
            self.conn.rollback()  # Rollback on error
            raise

    def commit(self):
        self.conn.commit()
