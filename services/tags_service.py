import sqlite3
from classes.tag_class import CreateTag, UpdateTag
from helpers import status_list, dict_factory


def get(id):
    try:
        int(id)
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute("SELECT * FROM tags WHERE id = ?", (id,)).fetchall()
        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


def get_all():
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute("SELECT * FROM tags").fetchall()
        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


def get_by_status(status, start_page, end_page, word=""):
    try:
        if status not in status_list:
            raise ValueError("Not in list")
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            """
            SELECT * FROM tags WHERE status = ? AND name LIKE ? ORDER BY name  
            LIMIT ?
            OFFSET ?
           """,
            (status_list[status], word, end_page, start_page),
        ).fetchall()
        count = connection.execute(
            """
        SELECT COUNT(*) as count FROM tags WHERE status = ? AND name LIKE ?
        """
        )
        connection.commit()
        return [res, count["count"]]
    except Exception as error:
        print(error)
        raise Exception(error)


def get_all_by_status(status):
    try:
        if status not in status_list:
            raise ValueError("Not in list")
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            """SELECT * FROM tags WHERE status = ?  ORDER BY name""",
            (status_list[status],),
        ).fetchall()

        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


def insert(obj):
    try:
        CreateTag(obj)
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            "INSERT INTO tags (name, description) VALUES (?, ?) RETURNING *",
            (obj["name"], obj["description"]),
        ).fetchall()
        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


def update(id, obj):
    try:
        UpdateTag(*obj)
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            "UPDATE tags SET name = ?, description = ? WHERE id = ? RETURNING *",
            (obj["name"], obj["description"], id),
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
            "DELETE * FROM tags WHERE id = ? RETURNING *", (id,)
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
            raise ValueError()
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            "UPDATE tags SET status = ? WHERE id = ? RETURNING *", (status, id)
        ).fetchall()
        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)

        # def tag_handler(tags):
        #     try:
        #         with sqlite3.connect('database.db') as connection:
        connection.row_factory = dict_factory


#             res = []
#             for tag in tags:
#                 tag_result = connection.execute(
#                     """
#                     SELECT * FROM tags WHERE name = ?
#                     """, (tag , )).fetchone()
#                 if (tag_result):
#                     res.append(tag_result)
#                 else:
#                     connection.execute(
#                     """
#                     INSERT INTO tags (name) VALUES (?)
#                     """, (tag , )).fetchone()
#                 connection.commit()
#             return res
#     except Exception as error:
#         print(error)
#         raise Exception(error)
