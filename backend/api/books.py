from flask_injector import inject
from data_access.db_access import get_books, insert_into_books
from pathlib import Path
from random import Random


@inject
def get_all_books():
    books = []
    for book in get_books():
        books.append(
            {
                "book_id": book[0],
                "title": book[1],
                "cover_path": "static/covers/" + book[2],
            }
        )
    return books, 200


@inject
def insert_book(cover_image, book_title):
    print(cover_image)
    if cover_image.filename.split(".")[-1].lower() not in [
        "jpeg",
        "jpg",
        "png",
        "webp",
    ]:
        return "Image extension not accepted", 400
    file_name = (
        cover_image.filename.split(".")[0]
        + "_"
        + str(Random().randint(1000, 9999))
        + "."
        + cover_image.filename.split(".")[-1]
    )
    try:
        with open(
            Path(
                ".",
                "static",
                "covers",
                file_name,
            ),
            "xb",
        ) as fp:
            cover_image.save(fp)
    except FileExistsError:
        return (
            "Cover with same name exists try with changing the cover image name.",
            400,
        )
    return insert_into_books(book_title, file_name), 200
