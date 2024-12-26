import psycopg2
from data_access.conn import get_conn_params


def execute_query(query, params=None):
    conn_params = get_conn_params()

    try:
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        data = cursor.fetchall()
        return data
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
    finally:
        if conn:
            cursor.close()
            conn.close()


def create_record(table, columns, values):
    columns_str = ", ".join(columns)
    placeholders = ", ".join(["%s"] * len(values))
    query = f"INSERT INTO {table} ({columns_str}) VALUES ({placeholders}) RETURNING *"
    result = execute_query(query, values)
    return result


def read_records(table, conditions=None):
    query = f"SELECT * FROM {table}"
    if conditions:
        query += f" WHERE {conditions}"
    results = execute_query(query)
    return results


def update_record(table, updates, conditions):
    updates_str = ", ".join([f"{column} = %s" for column in updates.keys()])
    query = f"UPDATE {table} SET {updates_str} WHERE {conditions} RETURNING *"
    values = list(updates.values())
    result = execute_query(query, values)
    return result


def delete_record(table, conditions):
    query = f"DELETE FROM {table} WHERE {conditions} RETURNING *"
    result = execute_query(query)
    return result


def tuples_to_dict(tuple_keys, tuples):
    return [dict(zip(tuple_keys, my_tuple)) for my_tuple in tuples]
