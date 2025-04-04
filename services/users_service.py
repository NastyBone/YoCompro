import sqlite3
import bcrypt
from helpers import dict_factory, like_string, limit_or_pagination


def get(id):
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            "SELECT id, name, email, role FROM users WHERE id = ?", (id,)
        ).fetchall()
        connection.commit()
        print(res)
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


def get_all(name, filter, start_page, end_page):
    try:
        if filter:
            filter_string = f"AND role = '{filter}'"
        print(filter)
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            f"""
            SELECT id, name, email, role, created_at FROM users
            WHERE name LIKE ?
            {filter_string if filter else ""}
            ORDER BY name
            {limit_or_pagination(False, start_page, end_page)}
            """,
            (like_string(name),),
        ).fetchall()

        count = connection.execute(
            f"""
            SELECT COUNT(*) as count FROM users
            WHERE name LIKE ?
            {filter_string if filter else ""}
            """,
            (like_string(name),),
        ).fetchone()
        connection.commit()
        return [res, count["count"]]
    except Exception as error:
        print(error)
        raise Exception(error)


def insert(obj):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(obj["password"].encode(), salt)
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?) RETURNING id, name, email, role",
            (obj["name"], obj["email"], hashed_password),
        ).fetchone()
        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


def update(id, obj):
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            "UPDATE users SET name = ?, email = ? WHERE id = ? RETURNING id, name, email, role",
            (obj["name"], obj["email"], id),
        ).fetchall()
        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


def delete(id):
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            "DELETE FROM users WHERE id = ? RETURNING *", (id,)
        ).fetchall()
        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


def get_id_by_email(email):
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            "SELECT id, name, email, role, password FROM users WHERE email = ?",
            (email,),
        ).fetchall()
        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


def update_role(id, role):
    try:
        print(id, role)
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            "UPDATE users SET role = ? WHERE id = ? RETURNING id, name, email, role",
            (role, id),
        ).fetchall()
        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


def get_with_password(id):
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            "SELECT id, name, email, role, password FROM users WHERE id = ?", (id,)
        ).fetchall()
        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


def update_password(id, password):
    try:
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode(), salt)
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            "UPDATE users SET password = ? WHERE id = ?", (hashed_password, id)
        ).fetchall()
        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


def check_ownership(id):
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            """
            UPDATE users 
            SET role = CASE 
              WHEN (SELECT COUNT(*) FROM bussiness WHERE user_id = ?) > 0 THEN 'OWNER' 
              ELSE 'CLIENT' 
           END 
        WHERE id = ?;""",
            (id, id),
        ).fetchall()
        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)
