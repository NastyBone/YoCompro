import sqlite3
from classes.rating_class import *
from helpers import dict_factory, limit_or_pagination


def get(id):
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute("SELECT * FROM ratings WHERE id = ?", (id,)).fetchall()

        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


def get_all():
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute("SELECT * FROM ratings").fetchall()

        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


def insert(obj):
    CreateRating(obj)
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            "INSERT INTO ratings (score, comment, user_id, bussiness_id, product_id) VALUES (?, ?, ?, ?, ?) RETURNING *",
            (
                obj["score"],
                obj.get("comment", None),
                obj["user_id"],
                obj.get("bussiness_id", None),
                obj.get("product_id", None),
            ),
        ).fetchall()

        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


def update(id, obj):
    UpdateRating(obj)
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            "UPDATE ratings SET score = ?, comment = ? WHERE id = ? RETURNING *",
            (obj["score"], obj["comment"], id),
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
            "DELETE FROM ratings WHERE id = ? RETURNING *", (id,)
        ).fetchall()

        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


# DONE: Get comment by user


def get_by_user(user_id, limited=False, start_page=None, end_page=None, order="DESC"):
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            f"""SELECT * FROM ratings WHERE user_id = ?
            {limit_or_pagination(limited, start_page, end_page)}
            """,
            (user_id,),
        ).fetchall()
        count = {"count": ""}
        if not limited:
            count = connection.execute(
                f""" 
           SELECT COUNT(*) as count FROM ratings WHERE  user_id = ?
            """,
                (user_id,),
            ).fetchone()
        connection.commit()
        return [res, count["count"]]
    except Exception as error:
        print(error)
        raise Exception(error)


# DONE: Load ratings for bussiness
def get_by_bussiness(
    bussiness_id,
    limited=False,
    start_page=None,
    end_page=None,
    order_rating="DESC",
    order_time="DESC",
):
    try:
        limited_select_user = ""
        limited_join_user = ""
        limited_comment = ""
        if not limited:
            limited_select_user = ", u.name, r.comment"
            limited_join_user = "JOIN users u ON r.user_id = u.id"
            limited_comment = "AND r.comment IS NOT NULL"

        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            f"""SELECT r.* {limited_select_user} FROM ratings 
            {limited_join_user}
            WHERE bussiness_id = ? 
            {limited_comment}
            ORDER BY score {order_rating} {order_time}
            {limit_or_pagination(limited, start_page, end_page)}""",
            (bussiness_id,),
        ).fetchall()
        count = {"count": ""}
        if not limited:
            count = connection.execute(
                f""" 
           SELECT COUNT(*) as count FROM ratings WHERE bussiness_id = ?
            """,
                (bussiness_id,),
            ).fetchone()
        connection.commit()
        return [res, count["count"]]
    except Exception as error:
        print(error)
        raise Exception(error)


# DONE: Load ratings for products
def get_by_product(
    product_id, limited=False, start_page=None, end_page=None, order="DESC"
):
    try:
        limited_select_user = ""
        limited_join_user = ""
        limited_comment = ""
        if not limited:
            limited_select_user = ", u.name, r.comment"
            limited_join_user = "JOIN users u ON r.user_id = u.id"
            limited_comment = "AND r.comment IS NOT NULL"
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            f"""SELECT r.* {limited_select_user} FROM ratings r
            {limited_join_user}
            WHERE product_id = ? 
            {limited_comment}
            ORDER BY score {order}
            {limit_or_pagination(limited, start_page, end_page)}""",
            (product_id,),
        ).fetchall()
        count = {"count": ""}
        if not limited:
            count = connection.execute(
                f""" 
           SELECT COUNT(*) as count FROM ratings WHERE product_id = ? 
            """,
                (product_id,),
            ).fetchone()
        connection.commit()
        return [res, count["count"]]
    except Exception as error:
        print(error)
        raise Exception(error)


# DONE: Load ratings for bussiness


def get_average_by_bussiness(bussiness_id):
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            """SELECT COUNT(score) as count, COALESCE(AVG(score), 0) as avg_score FROM bussiness b
                    JOIN ratings r ON r.bussiness_id = b.id
                    WHERE bussiness_id = ?""",
            (bussiness_id,),
        ).fetchone()

        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


# DONE: Load ratings for products
def get_average_by_product(product_id):
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            """SELECT COUNT(score) as count, COALESCE(AVG(score), 0) as avg_score FROM products p
                JOIN ratings r ON r.product_id = p.id
                WHERE product_id = ?""",
            (product_id,),
        ).fetchall()

        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


def delete_duplicate_ratings(user_id, bussiness_id, product_id):
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            "DELETE FROM ratings WHERE user_id = ? AND bussiness_id = ? OR product_id = ? RETURNING *",
            (user_id, bussiness_id, product_id),
        ).fetchall()

        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


def insert_rating(user_id, bussiness_id, product_id, score, comment=None):
    try:
        with sqlite3.connect("database.db") as connection:
            cursor = connection.cursor()

            # Intenta actualizar la calificación existente
            cursor.execute(
                """
                UPDATE ratings
                SET score = ?, comment = ?, created_at = CURRENT_TIMESTAMP
                WHERE user_id = ? AND bussiness_id = ? AND product_id = ?
            """,
                (score, comment, user_id, bussiness_id, product_id),
            )

            # Verifica si se actualizó alguna fila
            if cursor.rowcount == 0:
                # Si no se actualizó, inserta una nueva calificación
                cursor.execute(
                    """
                    INSERT INTO ratings (score, comment, user_id, bussiness_id, product_id)
                    VALUES (?, ?, ?, ?, ?)
                """,
                    (score, comment, user_id, bussiness_id, product_id),
                )

            connection.commit()
    except Exception as error:
        print(error)
        raise Exception(error)
