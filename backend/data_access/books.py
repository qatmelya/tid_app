from data_access.base_funcs import (
    create_record,
    read_records,
    delete_record,
    execute_query,
    tuples_to_dict,
)


def create_book(title, cover):
    return next(
        iter(
            tuples_to_dict(
                ["id", "title", "cover"],
                create_record("books", ["title", "cover"], [title, cover]),
            )
        ),
        None,
    )


def get_all_books():
    return tuples_to_dict(["id", "title", "cover"], read_records("books"))


def delete_book_by_id(book_id):
    return delete_record("books", f"id = {book_id}")


def get_books_and_favorited_counts():
    query = (
        "SELECT b.title, b.cover, COUNT(ufb.book_id) AS favorited_count "
        "FROM books b "
        "LEFT JOIN user_favorited_books ufb ON b.id = ufb.book_id "
        "GROUP BY b.id, b.title "
        "ORDER BY favorited_count DESC"
    )
    books_favorited_counts = execute_query(query)
    return tuples_to_dict(["title", "cover", "favorited_count"], books_favorited_counts)
