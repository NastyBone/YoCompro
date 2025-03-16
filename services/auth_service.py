from services.users_service import (
    get_id_by_email,
    insert,
    get_with_password,
    update_password,
)
from flask_login import login_user, logout_user, current_user
from classes.users_class import UserLogin
import bcrypt
from helpers import dict_factory
import sqlite3


def login(email, password):
    try:
        user = get_id_by_email(email)
        print(user == [])
        if user == []:
            raise ValueError("User Not Found")
        user = user[0]
        user_login = UserLogin(
            id=user["id"],
            name=user["name"],
            email=user["email"],
            role=user["role"],
            password=user["password"],
        )
        if bcrypt.checkpw(password.encode(), user_login["password"]):
            res = login_user(user_login, remember=True)
        else:
            raise ValueError("Password Does Not Match")
        return user["id"]
    except Exception as error:
        print(error)
        return error


def logout():
    logout_user()
    return True


def register(obj):
    return insert(obj)


def change_password(id, old_password, new_password):
    try:
        user = get_with_password(id)
        if bcrypt.checkpw(
            old_password,
            user[0][4],
        ):
            update_password(id, new_password)
        else:
            return ValueError("Password Does Not Match")
    except Exception as error:
        print(error)
        return error, 400


def verify_existing_email(email):
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
            res = connection.execute(
                "SELECT * FROM users WHERE email = ?", (email,)
            ).fetchall()
            return res != []
    except Exception as error:
        print(error)
        raise Exception(error)
