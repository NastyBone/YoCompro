import sqlite3
from helpers import dict_factory


def insert(image_name, brand_id, image_path, db_type):
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            f"INSERT INTO {db_type} (image_name, brand_id, image_path) VALUES (?, ?, ?) RETURNING id, image_name, brand_id, image_path",
            (image_name, brand_id, image_path),
        ).fetchone()
        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)
