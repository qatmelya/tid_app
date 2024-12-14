import psycopg2
from psycopg2 import sql


def create_tables():
    # Connection parameters
    conn_params = {
        "dbname": "postgres",
        "user": "postgres",
        "password": "123456",
        "host": "localhost",
        "port": "5432",
    }

    try:
        # Connect to the PostgreSQL server
        conn = psycopg2.connect(**conn_params)
        conn.autocommit = True
        cursor = conn.cursor()

        # Create database if it doesn't exist
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'TiD_db'")
        if not cursor.fetchone():
            cursor.execute('CREATE DATABASE "TiD_db"')
            print("Database 'TiD_db' created.")
        else:
            print("Database 'TiD_db' already exists.")

        # Close connection to default database and reconnect to TiD_db
        cursor.close()
        conn.close()
        conn_params["dbname"] = "TiD_db"
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()

        # Create tables
        tables = {
            "books": (
                "CREATE TABLE IF NOT EXISTS books ("
                "book_id SERIAL PRIMARY KEY,"
                "book_title VARCHAR(255) NOT NULL,"
                "cover_path TEXT"
                ")"
            ),
            "sentences": (
                "CREATE TABLE IF NOT EXISTS sentences ("
                "sentence_id SERIAL PRIMARY KEY,"
                "nth_sentence INT NOT NULL,"
                "book_id INT NOT NULL REFERENCES books(book_id),"
                "sentence TEXT NOT NULL,"
                "transcript TEXT"
                ")"
            ),
            "TiD_transcripts": (
                "CREATE TABLE IF NOT EXISTS TiD_transcripts ("
                "id SERIAL PRIMARY KEY,"
                "media_path TEXT NOT NULL,"
                "transcript TEXT"
                ")"
            ),
        }

        for table_name, table_query in tables.items():
            cursor.execute(table_query)
            print(f"Table '{table_name}' created or already exists.")

        # Commit changes
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
    finally:
        if conn:
            cursor.close()
            conn.close()
            print("Connection closed.")


if __name__ == "__main__":
    create_tables()
