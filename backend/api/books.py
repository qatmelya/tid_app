import os
from flask_injector import inject
from data_access.db_access import get_books, insert_into_books


@inject
def get_all_books():
    return get_books()


@inject
def insert_book(book_payload):
    book_title = book_payload["book_title"]
    cover_path = book_payload["cover_path"]
    return insert_into_books(book_title, cover_path)
