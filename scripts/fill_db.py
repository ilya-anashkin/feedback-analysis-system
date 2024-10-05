import os
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
SOURCE_TABLE = os.getenv('SOURCE_TABLE')
SOURCE_COLUMN_NAME = os.getenv('SOURCE_COLUMN_NAME')

def create_connection():
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
