from data_access.base_funcs import (
    create_record,
    read_records,
    delete_record,
    update_record,
    execute_query,
    tuples_to_dict,
)


def create_user_book_history(user_id, book_id, last_sentence_id):
    return create_record(
        "user_book_history",
        ["user_id", "book_id", "last_read_sentence_id"],
        [user_id, book_id, last_sentence_id],
    )


def get_all_user_book_history():
    return tuples_to_dict(
        ["id", "user_id", "book_id", "last_read_sentence_id"],
        read_records("user_book_history"),
    )


def get_user_book_history(user_id, book_id):
    return next(
        iter(
            tuples_to_dict(
                ["id", "user_id", "book_id", "last_read_sentence_id"],
                read_records(
                    "user_book_history", f"user_id = {user_id} AND book_id = {book_id}"
                ),
            )
        ),
        None,
    )


def update_user_book_history(user_id, book_id, last_sentence_id):
    if get_user_book_history(user_id, book_id) is None:
        return create_user_book_history(user_id, book_id, last_sentence_id)
    else:
        return update_record(
            "user_book_history",
            {"last_read_sentence_id": last_sentence_id},
            f"user_id = {user_id} AND book_id = {book_id}",
        )


def delete_user_book_history_by_id(history_id):
    return delete_record("user_book_history", f"id = {history_id}")
