from data_access import users
from datetime import datetime
from hashlib import sha512


def get_all_users():
    return users.get_all_users(), 200


def register(register_payload):
    if users.get_user_by_email(register_payload["email"]) is not None:
        return {"message": "User with same email already exists"}, 400

    user = users.create_user(
        register_payload["user_name"],
        sha512(register_payload["password"].encode("utf-8")).hexdigest(),
        register_payload["email"],
        datetime.now(),
    )
    return user["id"], 201


def login(login_payload):
    user = users.get_user_by_email(login_payload["email"])
    if not user:
        return {"message": "User with email not found"}, 400
    if (
        sha512(login_payload["password"].encode("utf-8")).hexdigest()
        == user["password"]
    ):
        return user["id"], 200
    else:
        return {"message": "Invalid credentials"}, 401
