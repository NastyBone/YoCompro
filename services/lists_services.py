import sqlite3
from helpers import dict_factory


def get(id):
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute("SELECT * FROM lists WHERE id = ?", (id,)).fetchall()

        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


def get_all():
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute("SELECT * FROM lists").fetchall()

        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


def insert(id):
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            "INSERT INTO lists (user_id) VALUES (?) RETURNING *", (id,)
        ).fetchall()

        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


# def update(id, obj):
#     try:
#         with sqlite3.connect('database.db') as connection:
#       connection.row_factory = dict_factory
#             res = connection.execute('UPDATE lists SET name = ?, email = ?, role = ? WHERE id = ? RETURNING *', (
#                 obj['name'], obj['email'], obj['role'], id)).fetchall()

#             connection.commit()
#             return res
#     except Exception as error:
#         print(error)
#         raise Exception(error)


def delete(id):
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            "DELETE FROM lists WHERE id = ? RETURNING *", (id,)
        ).fetchall()

        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


def get_by_user(user_id):
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            """
               SELECT l.id as list_id, s.price, s.discount, p.*, b.name as bussiness_name, b.address, s.id as stock_id FROM products p
               JOIN stocks s ON s.product_id = p.id
               JOIN lists_stocks ls ON s.id = ls.stock_id
               JOIN lists l ON l.id = ls.list_id
               JOIN bussiness b ON b.id = s.bussiness_id
               WHERE l.user_id = ?
               GROUP BY (p.id)
               """,
            (user_id,),
        ).fetchall()
        count = connection.execute(
            f""" 
            SELECT COUNT(*) as count FROM products p
                JOIN stocks s ON s.product_id = p.id
               JOIN lists_stocks ls ON s.id = ls.stock_id
               JOIN lists l ON l.id = ls.list_id
               JOIN bussiness b ON b.id = s.bussiness_id
               WHERE l.user_id = ?
            """,
            (user_id,),
        ).fetchone()
        connection.commit()
        return [res, count["count"]]
    except Exception as error:
        print(error)
        raise Exception(error)


def get_id_by_user(user_id):
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            """
               SELECT l.id as list_id FROM lists l
               WHERE l.user_id = ?
               """,
            (user_id,),
        ).fetchall()
        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


def insert_product(id, stock_id):
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            "INSERT INTO lists_stocks (list_id, stock_id) VALUES (?, ?) RETURNING *",
            (id, stock_id),
        ).fetchall()
        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


def delete_product(id, stock_id):
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            "DELETE FROM lists_stocks WHERE list_id = ? AND stock_id = ? RETURNING *",
            (id, stock_id),
        ).fetchall()
        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)
