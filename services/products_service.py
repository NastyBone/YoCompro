import sqlite3
from helpers import limit_or_pagination, type_list
from classes.product_class import *
from helpers import (
    status_list,
    dict_factory,
    like_string,
    slug_generator,
    product_filtering,
)


def get(id):
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute("SELECT * FROM products WHERE id = ?", id).fetchall()
        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


def get_all():
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute("SELECT * FROM products").fetchall()
        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


def insert(obj):
    try:
        CreateProduct(obj)
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            """
            INSERT INTO products
            (name, description, slug, brand_id)
            VALUES (?, ?, ?, ?) RETURNING *
            """,
            (
                obj["name"],
                obj["description"],
                slug_generator(obj["name"]),
                obj["brand_id"],
            ),
        ).fetchall()
        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


def update(id, obj):
    try:
        UpdateProduct(obj)
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            "UPDATE products SET name = ?, description = ?, slug = ?, brand_id = ? WHERE id = ? RETURNING *",
            (
                obj["name"],
                obj["description"],
                slug_generator(obj["name"]),
                obj["brand_id"],
                id,
            ),
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
            "DELETE FROM products WHERE id = ? RETURNING *", (id,)
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
            "UPDATE products SET status = ? WHERE id = ? RETURNING *", ([status], id)
        ).fetchall()
        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


def get_by_slug(name):
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            """SELECT p.*, COALESCE(AVG(score), 0) as avg_score FROM products p LEFT JOIN ratings r ON r.product_id = p.id WHERE slug LIKE ?""",
            (like_string(name),),
        ).fetchone()
        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


# DONE: Popular Products on City
def get_popular(city, start_page, end_page):
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            """
            SELECT p.*, score, COUNT(l.id) as count FROM products p
            JOIN stocks s ON s.product_id = p.id
            JOIN bussiness b ON s.bussiness_id = b.id
            JOIN lists_stocks l on l.stock_id = s.id
            JOIN ratings r ON r.product_id = p.id
            WHERE b.city LIKE ?
            AND p.status = "APPROVED"
            GROUP BY p.id
            ORDER BY count DESC
            LIMIT ?
            OFFSET ? 
            """,
            (like_string(city), end_page, start_page),
        ).fetchall()
        count = connection.execute(
            f""" 
            SELECT COUNT(*) as count FROM products p
            JOIN stocks s ON s.product_id = p.id
            JOIN bussiness b ON s.bussiness_id = b.id
            JOIN lists_stocks l on l.stock_id = s.id
            WHERE b.city LIKE ?
            AND p.status = "APPROVED"
            """,
            (like_string(city),),
        ).fetchone()
        connection.commit()
        return [res, count["count"]]
    except Exception as error:
        print(error)
        raise Exception(error)


# DONE: (Limited) Popular Products on City
def get_popular_limited(city):
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            """
            SELECT p.*, b.city, COUNT(l.id) as count, RANK() OVER (ORDER BY COUNT(l.id) DESC) as rank FROM products p
            JOIN stocks s on s.product_id = p.id
            JOIN bussiness b on s.bussiness_id = b.id
            JOIN lists_stocks l on l.stock_id = s.id
            WHERE b.city LIKE ?
            AND p.status = "APPROVED"
            GROUP BY p.id
            LIMIT 5
            """,
            (like_string(city),),
        ).fetchall()
        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


# DONE: Popular Products of that bussiness
def get_popular_by_bussiness(
    slug, bussiness, limited=False, start_page=None, end_page=None, order="DESC"
):
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            f"""
            SELECT p.*, COUNT(l.id) as count, s.price, s.discount FROM products p
            JOIN stocks s on s.product_id = p.id
            JOIN bussiness b on s.bussiness_id = b.id
            JOIN lists_stocks l on l.stock_id = s.id
            WHERE b.slug LIKE ?
            AND p.slug LIKE ?
            AND p.status = "APPROVED"
            GROUP BY p.id
            ORDER BY count {order}
            {limit_or_pagination(limited, start_page, end_page)}
            """,
            (
                like_string(bussiness),
                like_string(slug),
            ),
        ).fetchall()
        count = {"count": 0}
        if not limited:
            count = connection.execute(
                f""" 
            SELECT p.*, COUNT(l.id) as count FROM products p
            JOIN stocks s on s.product_id = p.id
            JOIN bussiness b on s.bussiness_id = s.id
            JOIN lists_stocks l on l.stock_id = s.id
            WHERE b.slug LIKE ?
            AND p.status = "APPROVED"
            """,
                (like_string(slug),),
            ).fetchone()
        connection.commit()

        return [res, count["count"]]
    except Exception as error:
        print(error)
        raise Exception(error)


# DONE: Popular Products by Brand
def get_popular_by_brand(
    slug, limited=False, start_page=None, end_page=None, order="DESC", word=""
):
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            f"""
            SELECT p.*, COUNT(l.id) as count FROM products p
            JOIN stocks s on s.product_id = p.id
            JOIN lists_stocks l on l.stock_id = s.id
            JOIN brands br on p.brand_id = br.id
            AND br.slug LIKE ?
            AND p.slug LIKE ?
            AND p.status = "APPROVED"
            GROUP BY p.id
            ORDER BY count {order}
            {limit_or_pagination(limited, start_page, end_page)}
            """,
            (like_string(slug), like_string(word)),
        ).fetchall()
        count = {"count": 0}
        if not limited:
            count = connection.execute(
                f""" 
            SELECT COUNT(*) as count FROM products p
           JOIN stocks s on s.product_id = p.id
            JOIN lists_stocks l on l.stock_id = s.id
            JOIN brands br on p.brand_id = br.id
            AND br.slug LIKE ?
            AND p.status = "APPROVED"
            """,
                (like_string(slug),),
            ).fetchone()
        connection.commit()
        return [res, count["count"]]
    except Exception as error:
        print(error)
        raise Exception(error)


##########################################

# DONE: Popular Products by Bussiness (limited)


# def get_popular_by_bussiness_limited(id):
#     try:
#         with sqlite3.connect("database.db") as connection:
#             connection.row_factory = dict_factory
#         res = connection.execute(
#             """
#             SELECT p.*, COUNT(l.id) as count FROM products p
#             JOIN stocks s on s.product_id = p.id
#             JOIN bussiness b on s.bussiness_id = b.id
#             JOIN lists_stocks l on l.stock_id = s.id
#             WHERE b.id = ?
#             AND p.status = "APPROVED"
#             GROUP BY p.id
#             ORDER BY count
#             LIMIT 5
#             """,
#             (id,),
#         ).fetchall()
#         connection.commit()
#         return res
#     except Exception as error:
#         print(error)
#         raise Exception(error)


# DONE: Popular Products by Brand (limited)
# def get_popular_by_brand_limited(brand_id, city):
#     try:
#         with sqlite3.connect("database.db") as connection:
#             connection.row_factory = dict_factory
#         res = connection.execute(
#             """
#             SELECT p.*, COUNT(l.id) as count FROM products p
#             JOIN stocks s on s.product_id = p.id
#             JOIN lists_stocks l on l.stock_id = s.id
#             JOIN brands br on p.brand_id = br.id
#             WHERE b.city LIKE ? AND br.id = ?
#             AND p.status = "APPROVED"
#             GROUP BY p.id
#             ORDER BY count
#             LIMIT 5
#             """,
#             (like_string(city), brand_id),
#         ).fetchall()
#         connection.commit()
#         return res
#     except Exception as error:
#         print(error)
#         raise Exception(error)


#############################################


# DONE: Top Rated Products on City
def get_top_rated(city, start_page, end_page):
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            """
            SELECT p.*, AVG(r.score) as avg_score FROM products p
            JOIN ratings r ON r.product_id = p.id
            JOIN stocks s on s.product_id = p.id
            JOIN bussiness b on s.bussiness_id = b.id
            WHERE b.city LIKE ?
            AND p.status = "APPROVED"
            ORDER BY avg_score DESC
            LIMIT ?
            OFFSET ? 
            """,
            (like_string(city), end_page, start_page),
        ).fetchall()
        count = connection.execute(
            f""" 
            SELECT COUNT(*) as count FROM products p
            JOIN ratings r ON r.product_id = p.id
            JOIN stocks s on s.product_id = p.id
            JOIN bussiness b on s.bussiness_id = b.id
            WHERE b.city LIKE ?
            AND p.status = "APPROVED"
            """,
            (like_string(city),),
        ).fetchone()
        connection.commit()
        return [res, count["count"]]
    except Exception as error:
        print(error)
        raise Exception(error)


# DONE: (Limited) Top Rated Products on City
def get_top_rated_limited(city):
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            """
            SELECT p.*, AVG(r.score) as avg_score, RANK() OVER (ORDER BY AVG(r.score) DESC) as rank
 FROM products p
            JOIN ratings r ON r.product_id = p.id
            JOIN stocks s ON s.product_id = p.id
            JOIN bussiness b ON b.id = s.bussiness_id
            WHERE b.city LIKE ?
            AND p.status = "APPROVED"
            LIMIT 5
            """,
            (like_string(city),),
        ).fetchall()
        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


# DONE: Top Rated Products By Brand
def get_top_rated_by_brand(
    slug, limited=False, start_page=None, end_page=None, order="DESC", word=""
):
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            f"""
            SELECT p.*, AVG(r.score) as avg_score, COUNT(r.score) as count FROM products p
            JOIN ratings r ON r.product_id = p.id
            JOIN brands br on p.brand_id = br.id
            WHERE br.slug LIKE ?
            AND p.slug LIKE ?
            AND p.status = "APPROVED"
            GROUP BY p.id
            ORDER BY avg_score {order}
            {limit_or_pagination(limited, start_page, end_page)}
            """,
            (like_string(slug), like_string(word)),
        ).fetchall()
        count = {"count": 0}
        if not limited:
            count = connection.execute(
                f""" 
            SELECT COUNT(*) as count FROM products p
            JOIN ratings r ON r.product_id = p.id
            JOIN brands br on p.brand_id = br.id
            WHERE br.slug LIKE ?
            AND p.status = "APPROVED"
            """,
                (like_string(slug),),
            ).fetchone()
        connection.commit()
        return [res, count["count"]]
    except Exception as error:
        print(error)
        raise Exception(error)


# DONE: Top Rated Products By Bussiness
def get_top_rated_by_bussiness(
    slug, bussiness, limited=False, start_page=None, end_page=None, order="DESC"
):
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            f"""
            SELECT p.*, AVG(r.score) as avg_score, s.price, s.discount FROM products p
            JOIN stocks s on s.product_id = p.id
            JOIN bussiness b on s.bussiness_id = b.id
            JOIN ratings r ON r.product_id = p.id
            WHERE b.slug LIKE ?
            AND p.slug LIKE ?
            AND p.status = "APPROVED"
            GROUP BY p.id
            ORDER BY avg_score  {order}
            {limit_or_pagination(limited, start_page, end_page)}
            """,
            (
                like_string(bussiness),
                like_string(slug),
            ),
        ).fetchall()
        count = {"count": 0}
        if not limited:
            count = connection.execute(
                f""" 
            SELECT COUNT(*) as count FROM products p
            JOIN stocks s on s.product_id = p.id
            JOIN bussiness b on s.bussiness_id = s.id
            JOIN ratings r ON r.product_id = p.id
            WHERE b.slug LIKE ?
            AND p.status = "APPROVED"
            """,
                (like_string(slug),),
            ).fetchone()
        connection.commit()
        return [res, count["count"]]
    except Exception as error:
        print(error)
        raise Exception(error)


######################################


# DONE Recent Added Products
def get_newest(city, start_page, end_page):
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            """
            SELECT p.* FROM products p
            JOIN stocks s on s.product_id = p.id
            JOIN bussiness b on s.bussiness_id = b.id
            WHERE b.city LIKE ?
            AND p.status = "APPROVED"
            GROUP BY p.id
            ORDER BY p.created_at DESC
            LIMIT ?
            OFFSET ? 
            """,
            (like_string(city), end_page, start_page),
        ).fetchall()
        count = connection.execute(
            f""" 
            SELECT COUNT(*) as count FROM products p
           JOIN stocks s on s.product_id = p.id
            JOIN bussiness b on s.bussiness_id = b.id
            WHERE b.city LIKE ?
            AND p.status = "APPROVED"
            """,
            (like_string(city),),
        ).fetchone()
        connection.commit()
        return [res, count["count"]]
    except Exception as error:
        print(error)
        raise Exception(error)


# DONE (Limited) Recent Added Products
def get_newest_limited(city):
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            """
            SELECT p.*, RANK() OVER (ORDER BY p.created_at) as rank FROM products p
            JOIN stocks s on s.product_id = p.id
            JOIN bussiness b on s.bussiness_id = b.id
            WHERE b.city LIKE ?
            AND p.status = "APPROVED"
            GROUP BY p.id
            LIMIT 5
            """,
            (like_string(city),),
        ).fetchall()
        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


# DONE Recent Added Products
def get_newest_by_brand(
    slug, limited=False, start_page=None, end_page=None, order="DESC", word=""
):
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            f"""
            SELECT p.* FROM products p
            JOIN brands br on p.brand_id = br.id
            WHERE br.slug LIKE ?
            AND p.status = "APPROVED"
            AND p.slug LIKE ?
            GROUP BY p.id
            ORDER BY p.created_at {order}
            {limit_or_pagination(limited, start_page, end_page)}
            """,
            (like_string(slug), like_string(word)),
        ).fetchall()
        count = {"count": 0}
        if not limited:
            count = connection.execute(
                f""" 
            SELECT COUNT(*) as count FROM products p
            JOIN brands br on p.brand_id = br.id
            WHERE br.slug LIKE ?
            AND p.status = "APPROVED"
            """,
                (like_string(slug),),
            ).fetchone()
        connection.commit()
        return [res, count["count"]]
    except Exception as error:
        print(error)
        raise Exception(error)


# DONE Recent Added Products
def get_newest_by_bussiness(
    slug, bussiness, limited=False, start_page=None, end_page=None, order="DESC"
):
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            f"""
            SELECT p.*, s.price, s.discount FROM products p
            JOIN stocks s on s.product_id = p.id
            JOIN bussiness b on s.bussiness_id = b.id
            WHERE b.slug LIKE ?
            AND p.slug LIKE ?
            AND p.status = "APPROVED"
            GROUP BY p.id
            ORDER BY p.created_at {order}
            {limit_or_pagination(limited, start_page, end_page)}
            """,
            (
                like_string(bussiness),
                like_string(slug),
            ),
        ).fetchall()
        count = {"count": 0}
        if not limited:
            count = connection.execute(
                f""" 
            SELECT COUNT(*) as count FROM products p
            JOIN stocks s on s.product_id = p.id
            JOIN bussiness b on s.bussiness_id = s.id
            WHERE b.slug LIKE ?
            AND p.status = "APPROVED"
            """,
                (like_string(slug),),
            ).fetchone()
        connection.commit()
        return [res, count["count"]]
    except Exception as error:
        print(error)
        raise Exception(error)


# DONE: Basic info


def get_with_details(id):
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            """SELECT p.*, br.name as brand_name, br.slug as brand_slug, br.country as brand_country FROM products p
JOIN brands br ON br.id = p.brand_id
           WHERE p.id = ?
            AND p.status = "APPROVED"
                      """,
            (id,),
        ).fetchall()
        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


# DONE: Get by brand
def get_by_brand(id):
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            """
            SELECT p.*, FROM products p
            JOIN brands br on p.brand_id = br.id
            WHERE br.id = ?
            AND p.status = "APPROVED"
            GROUP BY p.id
            ORDER BY p.name
            """,
            (id,),
        ).fetchall()
        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


# DONE: Popular Products of that owner
def get_popular_by_owner(
    owner_id,
    limited=False,
    start_page=None,
    end_page=None,
    order="DESC",
    word="",
    status="approved",
):
    try:
        print(owner_id, status_list[status], like_string(word))
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            f"""
            SELECT p.*, COUNT(l.id) as count FROM products p
            JOIN stocks s on s.product_id = p.id
            JOIN bussiness b on s.bussiness_id = b.id
            JOIN lists_stocks l on l.stock_id = s.id
            WHERE b.user_id = ?
            AND p.status LIKE ?
            AND p.slug LIKE ?
            GROUP BY p.id
            ORDER BY count {order}
            {limit_or_pagination(limited, start_page, end_page)}
            """,
            (owner_id, status_list[status], like_string(word)),
        ).fetchall()
        count = {"count": 0}
        if not limited:
            count = connection.execute(
                f""" 
            SELECT COUNT(*) as count FROM products p
            JOIN stocks s on s.product_id = p.id
            JOIN bussiness b on s.bussiness_id = b.id
            JOIN lists_stocks l on l.stock_id = s.id
            WHERE b.user_id = ?
            AND b.slug LIKE ?
            AND p.status = "APPROVED"
            """,
                (owner_id, like_string(word)),
            ).fetchone()
        connection.commit()
        return [res, count["count"]]
    except Exception as error:
        print(error)
        raise Exception(error)


# DONE: Popular Products of that owner
def get_top_rated_by_owner(
    owner_id,
    limited=False,
    start_page=None,
    end_page=None,
    order="DESC",
    word="",
    status="approved",
):
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            f"""
            SELECT p.*, AVG(score) as avg_score FROM products p
            JOIN ratings ON ratings.product_id = p.id
            JOIN stocks s on s.product_id = p.id
            JOIN bussiness b on s.bussiness_id = b.id
            WHERE b.user_id = ?
            AND p.status LIKE ?
            AND p.slug LIKE ?
            GROUP BY p.id
            ORDER BY avg_score {order}
            {limit_or_pagination(limited, start_page, end_page)}
            """,
            (owner_id, status_list[status], like_string(word)),
        ).fetchall()
        count = {"count": 0}
        if not limited:
            count = connection.execute(
                f""" 
            SELECT COUNT(*) as count FROM products p
            JOIN stocks s ON s.product_id = p.id
            JOIN bussiness b ON s.bussiness_id = b.id
            JOIN lists_stocks l on l.stock_id = s.id
            WHERE b.city LIKE ?
            AND p.slug LIKE ?
            AND p.status = "APPROVED"
            """,
                (owner_id, like_string(word)),
            ).fetchone()
        connection.commit()
        return [res, count["count"]]
    except Exception as error:
        print(error)
        raise Exception(error)


def get_by_search_tags(word, tags, start_page, end_page):
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
            if tags:
                tag_field = ",".join(["?"] * len(tags))
                res = connection.execute(
                    f"""
            SELECT p.* FROM products p
            JOIN tags_products tp ON tp.product_id = p.id
            WHERE tp.tag_id IN ({tag_field}) AND
            p.name LIKE ?
            AND p.status = "APPROVED"
            GROUP BY p.id
            HAVING COUNT(DISTINCT tp.tag_id) = ?
            LIMIT ?
            OFFSET ?
                """,
                    (*tags, like_string(word), len(tags), end_page, start_page),
                ).fetchall()
                count = connection.execute(
                    f""" 
                SELECT COUNT(*) as count FROM products p
            JOIN tags_products tp ON tp.product_id = p.id
            WHERE tp.tag_id IN ({tag_field}) AND
            p.name LIKE ?
            AND p.status = "APPROVED"
            HAVING COUNT(DISTINCT tp.tag_id) = ?""",
                    (*tags, like_string(word), len(tags)),
                ).fetchone()
            else:
                res = connection.execute(
                    f"""
           SELECT p.* FROM products p
           WHERE
           p.name LIKE ?
            AND p.status = "APPROVED"
           GROUP BY p.id
           LIMIT ?
           OFFSET ?
               """,
                    (like_string(word), end_page, start_page),
                ).fetchall()
            count = connection.execute(
                f""" 
            SELECT COUNT(*) as count FROM products p
            WHERE p.status = "APPROVED"
            AND p.name LIKE ?
            """,
                (like_string(word),),
            ).fetchone()
        connection.commit()
        return [res, count["count"]]
    except Exception as error:
        print(error)
        raise Exception(error)


def get_by_filter(type, slug, filter, start_page, end_page):

    try:
        if type == type_list["brands"]:
            return ""
        elif ():
            return ""
        else:
            with sqlite3.connect("database.db") as connection:
                connection.row_factory = dict_factory
        res = connection.execute(
            f"""SELECT * FROM products,
                WHERE slug LIKE ?
                AND p.status = "APPROVED"
                LIMIT ?
                OFFSET ?
                """,
            (like_string(slug), end_page, start_page),
        ).fetchall()

        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


def get_by_discounts(id):
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            """SELECT * FROM products p
            JOIN stocks s ON s.product_id = p.id
            WHERE p.id = ?
            AND p.status = "APPROVED"
            GROUP BY s.id
            ORDER BY s.discount DESC
            """,
            (id,),
        ).fetchall()

        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


def get_all_by_discounts(city):
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            """SELECT * FROM products p
            JOIN stocks s ON s.product_id = p.id
            JOIN bussiness b ON b.id = s.bussiness_id
            WHERE b.city LIKE ?
            AND p.status = "APPROVED"
            GROUP BY s.id
            ORDER BY s.discount DESC
            """,
            (like_string(city),),
        ).fetchall()

        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


def get_by_nearest(lat, lon, city):
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            """
SELECT *,
       ( 3959 * acos( cos( radians(?) ) * cos( radians(lat) ) * cos( radians(lon) - radians(?) ) + sin( radians(?) ) * sin( radians(lat) ) ) ) AS distance
JOIN stocks s ON p.id = s.product_id
JOIN bussiness b ON b.id = s.bussiness_id
FROM products p
WHERE city LIKE ?
AND p.status = "APPROVED"
ORDER BY distance ASC""",
            (lat, lon, lat, like_string(city)),
        ).fetchall()

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
            SELECT * FROM products WHERE status = ? AND name LIKE ? ORDER BY name  
            {limit_or_pagination(False, start_page, end_page)}
           """,
            (status_list[status], like_string(word)),
        ).fetchall()
        count = connection.execute(
            """
        SELECT COUNT(*) as count FROM products WHERE status = ? AND name LIKE ?
        """,
            (status_list[status], like_string(word)),
        ).fetchone()
        connection.commit()
        print(res)
        return [res, count["count"]]
    except Exception as error:
        print(error)
        raise Exception(error)


def search_by_bussiness(
    bussiness_slug,
    product_word,
    start_page,
    end_page,
    product_filter,
    order,
):
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            f""" SELECT p.*, s.price, s.discount, COUNT(l.id) as count FROM products p
                JOIN stocks s ON s.product_id = p.id
                JOIN bussiness b ON s.bussiness_id = b.id
                JOIN ratings r On r.bussiness_id = b.id
                JOIN lists_stocks l On l.stock_id = s.id
                WHERE b.slug LIKE ?
                AND p.name LIKE ? 
                AND b.status = "APPROVED" and p.status = "APPROVED"
                ORDER BY {product_filtering(product_filter, order)}
                {limit_or_pagination(False, start_page, end_page)}
           """,
            (like_string(bussiness_slug), like_string(product_word)),
        ).fetchall()
        count = connection.execute(
            """ SELECT COUNT(p.id) as count FROM bussiness b
                JOIN stocks s ON s.bussiness_id = b.id
                JOIN products p ON s.product_id = p.id
                WHERE p.slug LIKE ?
                AND b.name LIKE ? 
                AND b.status = "APPROVED" and p.status = "APPROVED" 
        """,
            (like_string(bussiness_slug), like_string(product_word)),
        ).fetchone()
        connection.commit()
        return [res, count["count"]]
    except Exception as error:
        print(error)
        raise Exception(error)


def tags_setter(product_id, tags):
    try:
        int(product_id)
        with sqlite3.connect("database.db") as connection:
            cursor = connection.cursor()
        cursor.execute(
            """DELETE FROM tags_products WHERE product_id = ?
            """,
            (product_id,),
        )
        connection.commit()
        tags_data = [(int(tag["id"]), int(product_id)) for tag in tags]
        print(tags_data)
        res = cursor.executemany(
            """INSERT INTO tags_products (tag_id, product_id) VALUES (?,?) """,
            (tags_data),
        ).fetchall()
        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)
