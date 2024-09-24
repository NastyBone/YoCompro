import sqlite3
from classes.rating_class import *
from helpers import dict_factory


def get(id):
    try:
        with sqlite3.connect('database.db') as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            'SELECT * FROM ratings WHERE id = ?', (id, )).fetchall()

        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


def get_all():
    try:
        with sqlite3.connect('database.db') as connection:
            connection.row_factory = dict_factory
        res = connection.execute('SELECT * FROM ratings').fetchall()

        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


def insert(obj):
    CreateRating(obj)
    try:
        with sqlite3.connect('database.db') as connection:
            connection.row_factory = dict_factory
        res = connection.execute('INSERT INTO ratings (score, comment, user_id, bussiness_id, product_id) VALUES (?, ?, ?, ?, ?) RETURNING *', (
            obj['score'], obj.get('comment', None), obj['user_id'], obj.get('bussiness_id', None), obj.get('product_id', None))).fetchall()

        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


def update(id, obj):
    UpdateRating(obj)
    try:
        with sqlite3.connect('database.db') as connection:
            connection.row_factory = dict_factory
        res = connection.execute('UPDATE ratings SET score = ?, comment = ? WHERE id = ? RETURNING *', (
            obj['score'], obj['comment'], id)).fetchall()

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
            'DELETE FROM ratings WHERE id = ? RETURNING *', (id, )).fetchall()

        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)

# DONE: Get comment by user


def get_by_user(user_id):
    try:
        with sqlite3.connect('database.db') as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            'SELECT * FROM ratings WHERE user_id = ?', (user_id, )).fetchall()

        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


# DONE: Load ratings for bussiness
def get_by_bussiness(bussiness_id, page_start, page_end):
    try:
        with sqlite3.connect('database.db') as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            'SELECT *, AVG(score) as avg_score FROM ratings WHERE bussiness_id = ? GROUP BY id LIMIT ?  OFFSET ?', (bussiness_id, page_end, page_start)).fetchall()

        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


# DONE: Load ratings for products
def get_by_product(product_id, page_start, page_end):
    try:
        with sqlite3.connect('database.db') as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            'SELECT *, AVG(score) as avg_score FROM ratings WHERE product_id = ? GROUP BY id LIMIT ? OFFSET ?', (product_id, page_end, page_start)).fetchall()

        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)

# DONE: Load ratings for bussiness


def get_average_by_bussiness(bussiness_id):
    try:
        with sqlite3.connect('database.db') as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            '''SELECT COUNT(score) as count, AVG(score) as avg_score FROM bussiness b
                    JOIN ratings r ON r.bussiness_id = b.id
                    WHERE bussiness_id = ?''', (bussiness_id, )).fetchall()

        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


# DONE: Load ratings for products
def get_average_by_product(product_id):
    try:
        with sqlite3.connect('database.db') as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            '''SELECT COUNT(score) as count, AVG(score) as avg_score FROM products p
                JOIN ratings r ON r.product_id = p.id
                WHERE product_id = ?''', (product_id, )).fetchall()

        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


def delete_duplicate_ratings(user_id, bussiness_id, product_id):
    try:
        with sqlite3.connect('database.db') as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            'DELETE FROM ratings WHERE user_id = ? AND bussiness_id = ? OR product_id = ? RETURNING *', (user_id, bussiness_id, product_id)).fetchall()

        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)
