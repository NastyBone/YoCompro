import sqlite3
import bcrypt
from helpers import dict_factory


def get(id):
    try:
        with sqlite3.connect('database.db') as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            'SELECT id, name, email, role FROM users WHERE id = ?', (id,)).fetchall()
        connection.commit()
        print(res)
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


def get_all():
    try:
        with sqlite3.connect('database.db') as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            'SELECT id, name, email, role  FROM users').fetchall()
        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


def insert(obj):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(obj['password'].encode(), salt)
    try:
        with sqlite3.connect('database.db') as connection:
            connection.row_factory = dict_factory
        res = connection.execute('INSERT INTO users (name, email, password) VALUES (?, ?, ?) RETURNING id, name, email, role', (
            obj['name'], obj['email'], hashed_password)).fetchall()
        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


def update(id, obj):
    try:
        with sqlite3.connect('database.db') as connection:
            connection.row_factory = dict_factory
        res = connection.execute('UPDATE users SET name = ?, email = ? WHERE id = ? RETURNING id, name, email, role', (
            obj['name'], obj['email'], id)).fetchall()
        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


def delete(id):
    try:
        with sqlite3.connect('database.db') as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            'DELETE FROM users WHERE id = ? RETURNING *', id).fetchall()
        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


def get_id_by_email(email):
    try:
        with sqlite3.connect('database.db') as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            'SELECT id, name, email, role, password FROM users WHERE email = ?', (email, )).fetchall()
        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


def update_role(id, role):
    try:
        with sqlite3.connect('database.db') as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            'UPDATE users SET role = ? WHERE id = ? RETURNING id, name, email, role', (id, role)).fetchall()
        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


def get_with_password(id):
    try:
        with sqlite3.connect('database.db') as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            'SELECT id, name, email, role, password FROM users WHERE id = ?', (id, )).fetchall()
        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


def update_password(id, password):
    try:
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode(), salt)
        with sqlite3.connect('database.db') as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            'UPDATE users SET password = ? WHERE id = ?', (hashed_password, id)).fetchall()
        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)
