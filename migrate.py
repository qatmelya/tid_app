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
                "id SERIAL PRIMARY KEY,"
                "title VARCHAR(255) NOT NULL,"
                "cover TEXT"
                ")"
            ),
            "users": (
                "CREATE TABLE IF NOT EXISTS users ("
                "id SERIAL PRIMARY KEY,"
                "name VARCHAR(255) NOT NULL,"
                "password TEXT NOT NULL,"
                "email VARCHAR(255) UNIQUE NOT NULL,"
                "last_access TIMESTAMP"
                ")"
            ),
            "sentences": (
                "CREATE TABLE IF NOT EXISTS sentences ("
                "id SERIAL PRIMARY KEY,"
                "nth_sentence INT NOT NULL,"
                "sentence TEXT NOT NULL,"
                "book_id INT NOT NULL REFERENCES books(id)"
                ")"
            ),
            "transcripts": (
                "CREATE TABLE IF NOT EXISTS transcripts ("
                "id SERIAL PRIMARY KEY,"
                "media_path TEXT NOT NULL,"
                "transcription TEXT"
                ")"
            ),
            "sentence_transcriptions": (
                "CREATE TABLE IF NOT EXISTS sentence_transcriptions ("
                "id SERIAL PRIMARY KEY,"
                "sentence_id INT NOT NULL REFERENCES sentences(id),"
                "transcript_id INT NOT NULL REFERENCES transcripts(id),"
                "nth_transcription INT NOT NULL"
                ")"
            ),
            "user_favorited_books": (
                "CREATE TABLE IF NOT EXISTS user_favorited_books ("
                "id SERIAL PRIMARY KEY,"
                "user_id INT NOT NULL REFERENCES users(id),"
                "book_id INT NOT NULL REFERENCES books(id)"
                ")"
            ),
            "user_book_history": (
                "CREATE TABLE IF NOT EXISTS user_book_history ("
                "id SERIAL PRIMARY KEY,"
                "user_id INT NOT NULL REFERENCES users(id),"
                "book_id INT NOT NULL REFERENCES books(id),"
                "last_read_sentence_id INT REFERENCES sentences(id)"
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
