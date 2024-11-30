import os
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

load_dotenv()

DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_NAME = "postgres"
DB_HOST = "localhost"
DB_PORT = 5432
SOURCE_TABLE = "data"
SOURCE_COLUMN_NAME = "text"

def create_connection():
    """
    Create a connection to the PostgreSQL database.

    Returns:
        conn: A psycopg2 connection object if the connection is successful,
              or None if the connection fails.
    """
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        print("Connection to database successful.")
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def setup_and_fill_database(conn):
    """
    Set up the database by creating a table and populating it with sample data.

    Args:
        conn: A psycopg2 connection object used to interact with the database.

    This function creates a table defined by the SOURCE_TABLE variable
    and populates it with predefined sample feedback data.
    """
    with conn:
        with conn.cursor() as cursor:
            # Создаем таблицу
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {SOURCE_TABLE} (
                    id SERIAL PRIMARY KEY,
                    {SOURCE_COLUMN_NAME} TEXT NOT NULL
                );
            """)
            print(f"Table {SOURCE_TABLE} created successfully.")

            # Наполняем таблицу данными
            sample_data = [
                "Отличный товар, очень доволен покупкой!",
                "Качество не соответствует ожиданиям.",
                "Прекрасная вещь, рекомендую всем!",
                "Не понравился, ожидал лучшего.",
                "Супер! Буду покупать еще раз."
            ]

            for text in sample_data:
                cursor.execute(sql.SQL(f"INSERT INTO {SOURCE_TABLE} (text) VALUES (%s);"), [text])
                print("Sample data successfully inserted")

if __name__ == "__main__":
    connection = create_connection()
    if connection:
        setup_and_fill_database(connection)
        connection.close()
