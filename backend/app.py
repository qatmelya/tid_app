import os
import connexion
from connexion.resolver import RestyResolver
from flask_cors import CORS
from flask import render_template
from flask import request, jsonify
from flask import flash, redirect, url_for
from werkzeug.utils import secure_filename
import requests
from pathlib import Path
from random import Random
from data_access import books, users
import sys
import json

app = connexion.App(__name__, specification_dir="swagger/")
CORS(app.app)
app.secret_key = "super_secret_key"
app.add_api("tid_language_docs.yaml", resolver=RestyResolver("api"))


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/add_book")
def add_book():
    return render_template("add_book.html")


@app.route("/reader_analytics")
def reader_analytics():
    daily_unique_visits_api_url = url_for(
        "/api.api_analytics_get_daily_unique_visits", _external=True
    )
    print(daily_unique_visits_api_url)
    daily_unique_visits_response = requests.get(daily_unique_visits_api_url)
    daily_unique_visits = daily_unique_visits_response.json()

    book_favorite_counts_api_url = url_for(
        "/api.api_analytics_get_book_favorite_counts", _external=True
    )
    book_favorite_counts_response = requests.get(book_favorite_counts_api_url)
    book_favorite_counts = book_favorite_counts_response.json()
    book_favorite_counts = sorted(
        book_favorite_counts, key=lambda x: x["favorited_count"], reverse=True
    )
    most_favorited_book = book_favorite_counts[0]
    most_favorited_book_title = most_favorited_book["title"]
    most_favorited_book_cover = most_favorited_book["cover"]

    return render_template(
        "reader_analytics.html",
        today_unique_visits=daily_unique_visits,
        most_favorited_book=most_favorited_book_title,
        most_favorited_book_cover=most_favorited_book_cover,
    )


@app.route("/book_catalog")
def book_catalog():
    api_url = url_for("/api.api_books_get_all_books", _external=True)
    response = requests.get(api_url)
    books = response.json()
    return render_template("book_catalog.html", books=books)


@app.route("/user_management")
def user_management():
    api_url = url_for("/api.api_users_get_all_users", _external=True)
    response = requests.get(api_url)
    users = response.json()
    return render_template("user_management.html", users=users)


@app.route("/delete_user/<int:user_id>")
def delete_user(user_id):
    users.delete_user_by_id(user_id)
    return redirect(url_for("user_management"))


@app.route("/add_book", methods=["POST"])
def add_book_post():
    title = request.form["title"]
    cover_image = request.files["cover_image"]
    book_content = request.files["book_content"]

    # Validate file types
    if cover_image.filename.split(".")[-1].lower() not in ["jpg", "png", "jpeg"]:
        return redirect(url_for("add_book_post"))
    if book_content.filename.split(".")[-1].lower() != "json":
        return redirect(url_for("add_book_post"))

    # Save files to server
    book_content_filename = secure_filename(book_content.filename)

    cover_image_filename = secure_filename(
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
                cover_image_filename,
            ),
            "xb",
        ) as fp:
            cover_image.save(fp)
    except FileExistsError:
        return (
            "Cover with same name exists try with changing the cover image name.",
            400,
        )
    book_id = books.create_book(title, cover_image_filename)["id"]

    Path(Path(sys.argv[0]).parent, "static", "tmp").mkdir(parents=True, exist_ok=True)
    with open(
        Path(
            Path(sys.argv[0]).parent,
            "static",
            "tmp",
            book_content_filename,
        ),
        "wb",
    ) as fp:
        book_content.save(fp)

    with open(
        Path(
            Path(sys.argv[0]).parent,
            "static",
            "tmp",
            book_content_filename,
        ),
        "r",
        encoding="utf-8",
    ) as fp:
        json_str = json.load(fp)
    os.remove(
        Path(
            Path(sys.argv[0]).parent,
            "static",
            "tmp",
            book_content_filename,
        )
    )

    for index, (sentence, files) in enumerate(json_str.items()):
        sentence_data = {
            "nth_sentence": str(index + 1),
            "book_id": str(book_id),
            "sentence": sentence,
        }
        created_sentence = requests.post(
            "http://127.0.0.1:2020/api/book_contents/add_sentence", json=sentence_data
        ).json()
        sentence_id = created_sentence["id"]
        for i, file in enumerate(files):
            transcript_id = requests.get(
                "http://127.0.0.1:2020/api/transcripts/get_by_transcript_string/"
                + file.split(".")[0]
            ).json()["id"]
            st_data = {
                "nth_transcription": i + 1,
                "sentence_id": sentence_id,
                "transcript_id": transcript_id,
            }
            requests.post(
                "http://127.0.0.1:2020/api/book_contents/add_sentence_transcription",
                json=st_data,
            )
    return redirect(url_for("book_catalog"))


app.run(port=int(os.environ.get("PORT", 2020)))
