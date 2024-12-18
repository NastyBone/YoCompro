import sqlite3
from helpers import dict_factory


def users_stats():
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            """WITH 
            general_count AS (SELECT COUNT(*) as count FROM users WHERE role IS NOT "ADMIN"),
            o_count AS (SELECT COUNT(*) as owner_count FROM users WHERE role = "OWNER"),
            u_count AS (SELECT COUNT(*) as user_count FROM users WHERE role = "CLIENT")

            SELECT count, owner_count, user_count FROM general_count, o_count, u_count""",
        ).fetchone()

        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


def bussiness_stats():
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            """WITH 
            general_count AS (SELECT COUNT(*) as count FROM bussiness),
            a_count AS (SELECT COUNT(*) as _approved FROM bussiness WHERE status = "APPROVED"),
            r_count AS (SELECT COUNT(*) as _rejected FROM bussiness WHERE status = "REJECTED"),
            rev_count AS (SELECT COUNT(*) as _review FROM bussiness WHERE status = "IN REVIEW")
            SELECT count, _approved as approved, _rejected as rejected, _review as review FROM general_count , a_count, r_count, rev_count""",
        ).fetchone()

        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


def products_stats():
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            """WITH 
            general_count AS (SELECT COUNT(*) as count FROM products),
            a_count AS (SELECT COUNT(*) as _approved FROM products WHERE status = "APPROVED"),
            r_count AS (SELECT COUNT(*) as _rejected FROM products WHERE status = "REJECTED"),
            rev_count AS (SELECT COUNT(*) as _review FROM products WHERE status = "IN REVIEW")
            SELECT count, _approved as approved, _rejected as rejected, _review as review FROM general_count , a_count, r_count, rev_count""",
        ).fetchone()

        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


def tags_stats():
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            """WITH 
            general_count AS (SELECT COUNT(*) as count FROM tags),
            a_count AS (SELECT COUNT(*) as _approved FROM tags WHERE status = "APPROVED"),
            r_count AS (SELECT COUNT(*) as _rejected FROM tags WHERE status = "REJECTED"),
            rev_count AS (SELECT COUNT(*) as _review FROM tags WHERE status = "IN REVIEW")
            SELECT count, _approved as approved, _rejected as rejected, _review as review FROM general_count , a_count, r_count, rev_count""",
        ).fetchone()

        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)
