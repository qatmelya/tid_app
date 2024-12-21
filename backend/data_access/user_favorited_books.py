from data_access.base_funcs import (
    create_record,
    read_records,
    delete_record,
    execute_query,
    tuples_to_dict,
)


def create_user_favorited_book(user_id, book_id):
    return tuples_to_dict(
        ["id", "user_id", "book_id"],
        create_record(
            "user_favorited_books", ["user_id", "book_id"], [user_id, book_id]
        ),
    )


def get_all_user_favorited_books():
    return tuples_to_dict(
        ["id", "user_id", "book_id"], read_records("user_favorited_books")
    )


def get_user_favorite_books(user_id):
    return tuples_to_dict(
        ["id", "user_id", "book_id"],
        read_records("user_favorited_books", f"user_id = '{user_id}'"),
    )


def delete_user_favorited_book(user_id, book_id):
    fav = next(
        iter(
            tuples_to_dict(
                ["id", "user_id", "book_id"],
                read_records(
                    "user_favorited_books",
                    f"user_id = {user_id} AND book_id = {book_id}",
                ),
            )
        ),
        None,
    )
    return tuples_to_dict(
        ["id", "user_id", "book_id"],
        delete_record("user_favorited_books", f"id = {fav['id']}"),
    )
