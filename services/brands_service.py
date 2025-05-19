import sqlite3
from classes.brand_class import *
from helpers import (
    like_string,
    status_list,
    dict_factory,
    limit_or_pagination,
)


def get(id):
    try:
        int(id)
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            """SELECT b.*, image_path as path FROM brands b 
                                 LEFT JOIN images_brands ib ON ib.brand_id = b.id WHERE b.id = ?""",
            (id,),
        ).fetchall()

        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


def get_all():
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            """SELECT b.*, image_path as path FROM brands b 
            LEFT JOIN images_brands ib ON ib.brand_id 
            WHERE status = 'APPROVED' """
        ).fetchall()

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
            (obj["name"], obj["slug"], obj["country"]),
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
            (obj["name"], obj["slug"], obj["country"], id),
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
            """SELECT b.*, image_path as path FROM brands b
            LEFT JOIN images_brands ib ON ib.brand_id = b.id
            WHERE name LIKE ? AND status = "APPROVED""",
            ("%" + name + "%",),
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
            SELECT b.*, COUNT(l.id) as count, image_path as path FROM brands b JOIN products p on p.brand_id = b.id 
            JOIN stocks s on s.product_id = p.id 
            LEFT JOIN images_brands ib on ib.brand_id = b.id
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
def get_popular_by_bussiness(bussiness_id, limited, start_page=None, end_page=None):
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            f"""
            SELECT br.*, COUNT(l.id) as count, image_path as path FROM brands br
            JOIN products p on p.brand_id = br.id
            LEFT JOIN images_brands ib on ib.brand_id = br.id
            JOIN stocks s on s.product_id = p.id 
            JOIN bussiness b on s.bussiness_id = b.id
            JOIN lists_stocks l on l.stock_id = s.id
            WHERE b.id = ? AND br.status = "APPROVED"
            GROUP BY br.id 
            ORDER BY count
            {limit_or_pagination(limited, start_page, end_page)}
            """,
            (bussiness_id,),
        ).fetchall()
        connection.commit()
        count = {"count": 0}
        if limited:
            count = connection.execute(
                f"""
            SELECT COUNT(*) as count FROM brands br 
            LEFT JOIN images_brands ib on ib.brand_id = br.id
            JOIN products p on p.brand_id = br.id 
            JOIN stocks s on s.product_id = p.id 
            JOIN bussiness b on s.bussiness_id = b.id 
            WHERE b.id = ? AND br.status = 'APPROVED'""",
                (bussiness_id,),
            ).fetchone()
        return [res, count["count"]]
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
            SELECT br.*, image_path as path FROM brands br
            LEFT JOIN images_brands ib on ib.brand_id = br.id
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


def get_with_details(slug):
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            """SELECT br.*, image_path as path FROM brands br
            LEFT JOIN images_brands ib ON ib.brand_id = br.id
           WHERE br.slug LIKE ?
            AND br.status = "APPROVED"
                      """,
            (like_string(slug),),
        ).fetchone()
        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


def get_by_status(status, start_page, end_page, word):
    try:
        if status not in status_list:
            raise ValueError("Not in list")
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            f"""
            SELECT br.*, image_path as path FROM brands br
            LEFT JOIN images_brands ib ON ib.brand_id = br.id
            WHERE status = ? AND name LIKE ? ORDER BY name  
            {limit_or_pagination(False, start_page, end_page)}
           """,
            (status_list[status], like_string(word)),
        ).fetchall()
        count = connection.execute(
            """
        SELECT COUNT(*) as count FROM brands br
        LEFT JOIN images_brands ib ON ib.brand_id = br.id
        WHERE status = ? AND name LIKE ?
        """,
            (status_list[status], like_string(word)),
        ).fetchone()
        connection.commit()
        return [res, count["count"]]
    except Exception as error:
        print(error)
        raise Exception(error)
