import requests

server_url = "http://127.0.0.1:2020/"


def get_books():
    books = requests.get(server_url + "v1.0/books/get_all_books")
    return books.json()


def get_book_content_by_id(book_id):
    books = requests.get(server_url + "v1.0/book_contents/" + str(book_id))
    print(books.json())
