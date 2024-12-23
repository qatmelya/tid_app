from datetime import datetime
from data_access.base_funcs import (
    create_record,
    read_records,
    delete_record,
    execute_query,
    tuples_to_dict,
)


def create_user(user_name, password, email, last_access):
    return create_record(
        "users",
        ["name", "password", "email", "last_access"],
        [user_name, password, email, last_access],
    )


def get_all_users():
    return tuples_to_dict(
        ["id", "name", "password", "email", "last_access"], read_records("users")
    )


def get_user_by_email(email):
    return next(
        iter(
            tuples_to_dict(
                ["id", "name", "password", "email", "last_access"],
                read_records("users", f"email = '{email}'"),
            )
        ),
        None,
    )


def get_user_by_id(user_id):
    return next(
        iter(
            tuples_to_dict(
                ["id", "name", "password", "email", "last_access"],
                read_records("users", f"id = {user_id}"),
            )
        ),
        None,
    )


def delete_user_by_id(user_id):
    return delete_record("users", f"id = {user_id}")


def get_todays_unique_visitors():
    # Get the current date
    today = datetime.now().date()

    # Execute query to fetch unique users who accessed today
    query = "SELECT COUNT(DISTINCT id) FROM users " "WHERE DATE(last_access) = %s"
    unique_visitors = execute_query(query, [today])
    return unique_visitors[0][0]
