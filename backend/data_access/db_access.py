import psycopg2


def _get_conn_params():
    conn_params = {
        "dbname": "TiD_db",
        "user": "postgres",
        "password": "123456",
        "host": "localhost",
        "port": "5432",
    }
    return conn_params


def insert_into_books(book_title, cover_path):
    conn_params = _get_conn_params()

    try:
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()
        query = (
            "INSERT INTO books (book_title, cover_path) "
            "VALUES (%s, %s) RETURNING book_id"
        )
        cursor.execute(query, (book_title, cover_path))
        book_id = cursor.fetchone()[0]
        conn.commit()
        return book_id

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
    finally:
        if conn:
            cursor.close()
            conn.close()


def insert_into_sentences(nth_sentence, book_id, sentence, transcript):
    conn_params = _get_conn_params()

    try:
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()
        query = (
            "INSERT INTO sentences (nth_sentence, book_id, sentence, transcript) "
            "VALUES (%s, %s, %s, %s) RETURNING sentence_id"
        )
        cursor.execute(query, (nth_sentence, book_id, sentence, transcript))
        sentence_id = cursor.fetchone()[0]
        conn.commit()
        return sentence_id

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
    finally:
        if conn:
            cursor.close()
            conn.close()


def insert_into_tid_transcripts(media_path, transcript):
    conn_params = _get_conn_params()

    try:
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()
        query = (
            "INSERT INTO TiD_transcripts (media_path, transcript) "
            "VALUES (%s, %s) RETURNING id"
        )
        cursor.execute(query, (media_path, transcript))
        transcript_id = cursor.fetchone()[0]
        conn.commit()
        print(f"Inserted into TiD_transcripts with id: {transcript_id}")
        return transcript_id

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
    finally:
        if conn:
            cursor.close()
            conn.close()
            print("Connection closed.")


def get_books():
    # Connection parameters
    conn_params = _get_conn_params()
    try:
        # Connect to the PostgreSQL server
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()

        # Query to fetch sentences ordered by nth_sentence
        query = "SELECT * FROM books "

        cursor.execute(query)
        books = cursor.fetchall()
        return books

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
    finally:
        if conn:
            cursor.close()
            conn.close()


def get_sentences_by_book_id(book_id):
    # Connection parameters
    conn_params = _get_conn_params()
    try:
        # Connect to the PostgreSQL server
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()

        # Query to fetch sentences ordered by nth_sentence
        query = (
            "SELECT nth_sentence, sentence, transcript "
            "FROM sentences "
            "WHERE book_id = %s "
            "ORDER BY nth_sentence"
        )

        cursor.execute(query, (book_id,))
        sentences = cursor.fetchall()
        print(sentences)
        return sentences

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
    finally:
        if conn:
            cursor.close()
            conn.close()


if __name__ == "__main__":
    print(get_books())
    print(get_sentences_by_book_id(0))
