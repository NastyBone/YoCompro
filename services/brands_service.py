import sqlite3
from classes.brand_class import *
from helpers import status_list, dict_factory, slug_builder


def get(id):
    try:
        int(id)
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute("SELECT * FROM brands WHERE id = ?", (id,)).fetchall()

        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


def get_all():
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute("SELECT * FROM brands").fetchall()

        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


def insert(obj):
    try:
        CreateBrand(obj)
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            "INSERT INTO brands (name, slug, country) VALUES (?, ?, ?) RETURNING *",
            (obj["name"], slug_builder(obj["name"]), obj["country"]),
        ).fetchall()

        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


def update(id, obj):
    try:
        int(id)
        UpdateBrand(obj)
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            "UPDATE brands SET name = ?, slug = ?, country = ? WHERE id = ? RETURNING *",
            (obj["name"], slug_builder(obj["name"]), obj["country"], id),
        ).fetchall()

        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


def delete(id):
    try:
        int(id)
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            "DELETE FROM brands WHERE id = ? RETURNING *", (id,)
        ).fetchall()

        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


def update_status(id, status):
    try:
        int(id)
        if status not in status_list:
            raise ValueError("Not in list")
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        print(status)
        res = connection.execute(
            "UPDATE brands SET status = ? WHERE id = ? RETURNING *",
            (status_list[status], id),
        ).fetchall()

        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


def get_by_name(name):
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            'SELECT * FROM brands WHERE name LIKE = ? AND status = "APPROVED"',
            ("%" + name + "%"),
        ).fetchall()

        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


def get_popular():
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            """
            SELECT b.*, COUNT(l.id) as count FROM brands b JOIN products p on p.brand_id = b.id 
            JOIN stocks s on s.product_id = p.id 
            JOIN lists_stocks l on l.stock_id = s.id 
            GROUP BY b.id 
            ORDER BY count
            """
        ).fetchall()

        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


# DONE: Popular Brands of that bussiness
def get_popular_by_bussiness(bussiness_id):
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            """
            SELECT br.*, COUNT(l.id) as count FROM brands br
            JOIN products p on p.brand_id = br.id
            JOIN stocks s on s.product_id = p.id 
            JOIN bussiness b on s.bussiness_id = b.id
            JOIN lists_stocks l on l.stock_id = s.id
            WHERE b.id = ? AND br.status = "APPROVED"
            GROUP BY br.id 
            ORDER BY count
            """,
            (bussiness_id,),
        ).fetchall()
        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


# DONE: Brand basic info


def get_by_product_id(product_id):
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            """
            SELECT br.* FROM brands br
            JOIN products p on p.brand_id = br.id
            WHERE p.id = ? AND br.status = "APPROVED"
            GROUP BY br.id
            """,
            (product_id,),
        ).fetchall()
        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


def get_with_details(id):
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            """SELECT * FROM brands br
           WHERE br.id = 1
            AND br.status = "APPROVED"
                      """,
            (id,),
        ).fetchall()
        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)
