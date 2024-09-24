import sqlite3
from classes.stock_class import *
from helpers import dict_factory, like_string


def get(id):
    try:
        with sqlite3.connect('database.db') as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            'SELECT * FROM stocks WHERE id = ?', (id, )).fetchall()

        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


def get_all():
    try:
        with sqlite3.connect('database.db') as connection:
            connection.row_factory = dict_factory
        res = connection.execute('SELECT * FROM stocks').fetchall()

        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


def insert(obj):
    try:
        CreateStock(obj)
        with sqlite3.connect('database.db') as connection:
            connection.row_factory = dict_factory
        res = connection.execute('INSERT INTO stocks (quantity, price, discount, product_id, bussiness_id) VALUES (?, ?, ?, ?, ?) RETURNING *', (
            obj['quantity'], obj['price'], obj['discount'], obj['product_id'], obj['bussiness_id'])).fetchall()

        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


def update(id, obj):
    try:
        UpdateStock(obj)
        with sqlite3.connect('database.db') as connection:
            connection.row_factory = dict_factory
        res = connection.execute('UPDATE stocks SET discount = ?, quantity = ?, price = ? WHERE id = ? RETURNING *', (
            obj['discount'], obj['quantity'], obj['price'], id)).fetchall()

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
            'DELETE FROM stocks WHERE id = ? RETURNING *', (id, )).fetchall()

        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


def get_by_bussiness(id, owner_id, page_start, page_end):
    try:
        with sqlite3.connect('database.db') as connection:
            connection.row_factory = dict_factory
        res = connection.execute("""
            SELECT * FROM stocks s
            JOIN bussiness b ON s.bussiness_id = b.id
            JOIN products p ON s.product_id = p.id
            WHERE 
            b.id = ? AND
            b.user_id = ?
            ORDER BY quantity
            LIMIT ? 
            OFFSET ?
            """, (id, owner_id, page_end, page_start)).fetchall()

        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)
