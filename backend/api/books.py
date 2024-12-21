from data_access import books, user_favorited_books
from pathlib import Path
from random import Random
import sys


def get_all_books():
    return books.get_all_books(), 200


def get_user_favorite_books(user_id):
    return user_favorited_books.get_user_favorite_books(user_id), 200


def add_favorite_book(favorite_payload):
    return user_favorited_books.create_user_favorited_book(
        favorite_payload["user_id"], favorite_payload["book_id"]
    ), 200


def remove_favorite_book(favorite_payload):
    return user_favorited_books.delete_user_favorited_book(
        favorite_payload["user_id"], favorite_payload["book_id"]
    ), 200


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
    Path(Path(sys.argv[0]).parent, "static", "covers").mkdir(
        parents=True, exist_ok=True
    )
    try:
        with open(
            Path(
                Path(sys.argv[0]).parent,
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
    return books.create_book(book_title, file_name), 200
