from data_access import books
from data_access import users


def get_daily_unique_visits():
    unique_visitor = users.get_todays_unique_visitors()
    return unique_visitor, 200


def get_book_favorite_counts():
    return books.get_books_and_favorited_counts(), 200
