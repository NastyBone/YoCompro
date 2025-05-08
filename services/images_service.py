import os
import sqlite3
from helpers import dict_factory


def insert(image_name, object_id, image_path, db_type, column_type):
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            f"INSERT INTO {db_type} (image_name, {column_type}, image_path) VALUES (?, ?, ?) RETURNING id, image_name, {column_type}, image_path",
            (image_name, object_id, image_path),
        ).fetchone()
        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


def update(
    image_name,
    object_id,
    image_path,
    db_type,
    column_type,
):
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        cursor = connection.cursor()
        data = cursor.execute(
            f"SELECT * FROM {db_type} WHERE {column_type} = ?",
            (object_id,),
        ).fetchone()
        res = cursor.execute(
            f"UPDATE {db_type} SET image_name = ?, image_path = ? WHERE {column_type} = ? RETURNING id, image_name, {column_type}, image_path",
            (
                image_name,
                image_path,
                object_id,
            ),
        ).fetchall()
        if cursor.rowcount == 0:
            res = cursor.execute(
                f"INSERT INTO {db_type} (image_name, {column_type}, image_path) VALUES (?, ?, ?) RETURNING id, image_name, {column_type}, image_path",
                (image_name, object_id, image_path),
            ).fetchall()
        connection.commit()
        if data:
            os.remove(data["image_path"][1:])
        return res
    except Exception as error:
        print(error)
        raise Exception(error)
