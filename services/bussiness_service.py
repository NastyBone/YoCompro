import sqlite3
from classes.bussiness_class import *
from helpers import status_list, dict_factory, like_string, slug_builder


def get(id):
    try:
        int(id)
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            "SELECT * FROM bussiness WHERE id = ?", (id,)
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
        res = connection.execute("SELECT * FROM bussiness").fetchall()

        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


def insert(obj):
    try:
        CreateBussiness(obj)
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            """
            INSERT INTO bussiness
            (name, email, description, slug, address,
             phone, rif, lat, lon, city, user_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) RETURNING *
            """,
            (
                obj["name"],
                obj["email"],
                obj["description"],
                slug_builder(obj["name"]),
                obj["address"],
                obj["phone"],
                obj["rif"],
                obj["lat"],
                obj["lon"],
                obj["city"],
                obj["user_id"],
            ),
        ).fetchall()

        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


def update(id, obj):
    try:
        int(id)
        UpdateBussiness(obj)
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            "UPDATE bussiness SET name = ?, email = ?,description = ?, address = ?, phone = ?, rif = ?, lat = ?, lon = ?, city = ?, slug = ? WHERE id = ? RETURNING *",
            (
                obj["name"],
                obj["email"],
                obj["description"],
                obj["address"],
                obj["phone"],
                obj["rif"],
                obj["lat"],
                obj["lon"],
                obj["city"],
                slug_builder(obj["slug"]),
                id,
            ),
        ).fetchall()

        connection.commit()
        print(res)
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
            "DELETE FROM bussiness WHERE id = ? RETURNING *", (id,)
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
            "UPDATE bussiness SET status = ? WHERE id = ? RETURNING *;",
            (status_list[status], id),
        ).fetchall()

        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


def get_by_slug(slug):
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            "SELECT * FROM bussiness WHERE slug LIKE ? AND status = 'APPROVED'",
            (like_string(slug),),
        ).fetchone()

        connection.commit()
        print(res)
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


# DONE: Popular Bussiness with that brand
def get_popular_by_brand(city, slug, page_start, page_end):
    try:

        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            """
            SELECT b.*, COUNT(l.id) as count FROM bussiness b
            JOIN stocks s on s.bussiness_id = b.id 
            JOIN lists_stocks l on l.stock_id = s.id 
            JOIN products p on s.product_id = p.id
            JOIN brands br on p.brand_id = br.id
            WHERE city LIKE ? AND br.slug LIKE ?
            AND b.status = "APPROVED"
            GROUP BY b.id 
            ORDER BY count DESC
            LIMIT ?
            OFFSET ?
            """,
            (
                like_string(city),
                like_string(slug),
                page_end,
                page_start,
            ),
        ).fetchall()
        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)
        # SELECT b.*, COUNT(l.id) as count FROM bussiness b
        # JOIN stocks s on s.bussiness_id = b.id
        # JOIN lists_stocks l on l.stock_id = s.id
        # JOIN products p on s.product_id = p.id
        # JOIN brands br on p.brand_id = br.id
        # WHERE b.city = ? AND br.slug = ?
        # GROUP BY b.id
        # ORDER BY count
        # LIMIT ?
        # OFFSET ?


# DONE: Popular Bussiness on City


def get_popular(city, start_page, end_page):
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            """
            SELECT b.*, COUNT(l.id) as count FROM bussiness b
            JOIN stocks s on s.bussiness_id = b.id 
            JOIN lists_stocks l on l.stock_id = s.id 
            WHERE b.city LIKE ?
            AND b.status = "APPROVED"
            GROUP BY b.id 
            ORDER BY count
            LIMIT ?
            OFFSET ?
            """,
            (like_string(city), end_page, start_page),
        ).fetchall()

        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


# DONE: (Limited) Popular Bussiness on City ### TRY POLYMORPH
def get_popular_limited(city):
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            """
            SELECT b.*, COUNT(l.id) as count , RANK() OVER (ORDER BY COUNT(l.id) DESC) as rank
 FROM bussiness b
            JOIN stocks s on s.bussiness_id = b.id 
            JOIN lists_stocks l on l.stock_id = s.id 
            WHERE b.city LIKE ?
            AND b.status = "APPROVED"
            GROUP BY b.id 
            LIMIT 5
            """,
            (like_string(city),),
        ).fetchall()

        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


# DONE: Top Rated Bussiness on City
def get_top_rated(city, start_page, end_page):
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            """
            SELECT b.*, AVG(r.score) as avg_score FROM bussiness b
            JOIN ratings ON r.bussiness_id = b.id
            WHERE b.city LIKE ?
            AND b.status = "APPROVED"
            GROUP BY b.id 
            ORDER BY count
            LIMIT ?
            OFFSET ?
            """,
            (like_string(city), end_page, start_page),
        ).fetchall()

        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


# DONE: (Limited) Top Rated Bussiness on City
def get_top_rated_limited(city):
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            """
            SELECT b.*, AVG(r.score) as avg_score FROM bussiness b
            JOIN ratings r ON r.bussiness_id = b.id
            WHERE b.city LIKE ?
            AND b.status = "APPROVED"
            GROUP BY b.id 
            ORDER BY avg_score
            LIMIT 5
            """,
            (like_string(city),),
        ).fetchall()

        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


# DONE: Most Discounts Bussiness on City
def get_by_most_discount(city, start_page, end_page):
    try:

        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            """
            SELECT b.*, AVG(s.discount) as avg_disc FROM bussiness b
            JOIN stocks s ON s.bussiness_id = b.id
            WHERE b.city LIKE ?
            AND b.status = "APPROVED"
            GROUP BY b.id
            ORDER BY avg_disc DESC
            LIMIT ?
            OFFSET ?
            """,
            (like_string(city), end_page, start_page),
        ).fetchall()

        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


# DONE: (Limited) Most Discounts Bussiness on City
def get_by_most_discount_limited(city):
    try:

        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            """
            SELECT b.*, AVG(s.discount) as avg_disc, RANK() OVER (ORDER BY AVG(s.discount) DESC) as rank
            FROM bussiness b
            JOIN stocks s ON s.bussiness_id = b.id
            WHERE b.city LIKE ?
            AND b.status = "APPROVED"
            LIMIT 5
            """,
            ((like_string(city)),),
        ).fetchall()

        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


# DONE Top discounts of that bussiness
def get_most_discount_by_bussiness(bussiness_id):
    try:

        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            """
            SELECT p.*, AVG(s.discount) as avg_disc FROM products p
            JOIN stocks s ON s.product_id = p.id
            JOIN bussiness b ON b.id = s.bussinesS_id
            WHERE b.id = ?
            AND b.status = "APPROVED"
            ORDER BY avg_disc DESC
            """,
            (bussiness_id,),
        ).fetchall()

        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


# DONE: Popular Bussiness of that owner
def get_by_owner_popular(
    owner_id, limited=False, start_page=None, end_page=None, order="DESC"
):
    try:
        pagination_clause = ""
        limited_clause = ""
        if limited:
            limited_clause = "LIMIT 5"
        if start_page and end_page:
            pagination_clause = f"LIMIT {end_page} OFFSET {start_page}"
        int(owner_id)
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            f"""
            SELECT b.*, COUNT(l.id) as count FROM bussiness b
            JOIN stocks s on s.bussiness_id = b.id
            JOIN lists_stocks l on l.stock_id = s.id
            WHERE b.user_id = ?
            AND b.status = "APPROVED"
            GROUP BY b.id
            ORDER BY count {order}
            {limited_clause}
            {pagination_clause}
            """,
            (owner_id,),
        ).fetchall()

        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


# DONE: Top rated Bussines
def get_by_owner_top_rated(
    owner_id, limited=False, start_page=None, end_page=None, order="DESC"
):
    try:
        int(owner_id)
        limited_clause = ""
        pagination_clause = ""
        if limited:
            limited_clause = "LIMIT 5"
        if start_page and end_page:
            pagination_clause = f"LIMIT {end_page} OFFSET {start_page}"
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            f"""
            SELECT b.*, AVG(score) as avg_score FROM bussiness b
            JOIN ratings ON ratings.bussiness_id = b.id
            WHERE b.user_id = ?
            AND b.status = "APPROVED"
            ORDER BY avg_score {order}
            {limited_clause}
            {pagination_clause}
            """,
            (owner_id,),
        ).fetchall()

        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


# DONE: All Bussiness of the owner
def get_by_owner(owner_id, start_page, end_page):
    try:
        int(owner_id)
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            """SELECT * FROM bussiness WHERE user_id = ? 
            AND b.status = "APPROVED"
            LIMIT ? OFFSET ? """,
            (owner_id, end_page, start_page),
        ).fetchall()

        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


# DONE: Search


def get_by_search_tags(word, tags, start_page, end_page):
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
            if tags:
                tag_field = ",".join(["?"] * len(tags))
                res = connection.execute(
                    f"""
            SELECT b.* FROM bussiness b
            JOIN tags_bussiness tb ON tb.bussiness_id = b.id
            WHERE tb.tag_id IN ({tag_field}) AND
            b.name LIKE ?
            AND b.status = "APPROVED"
            GROUP BY b.id
            HAVING COUNT(DISTINCT tb.tag_id) = ?
            LIMIT ?
            OFFSET ?
                """,
                    (*tags, like_string(word), len(tags), end_page, start_page),
                ).fetchall()
                count = connection.execute(
                    f""" 
                SELECT COUNT(*) as count FROM bussiness b
           JOIN tags_bussiness tb ON tb.bussiness_id = b.id
            WHERE tb.tag_id IN ({tag_field}) AND
            b.name LIKE ?
            AND b.status = "APPROVED"
            GROUP BY b.id
            HAVING COUNT(DISTINCT tb.tag_id) = ?""",
                    (*tags, like_string(word), len(tags)),
                ).fetchone()
            else:
                res = connection.execute(
                    f"""
            SELECT b.* FROM bussiness b
            WHERE
            b.name LIKE ?
            AND b.status = "APPROVED"
            GROUP BY b.id
            LIMIT ?
            OFFSET ?
                """,
                    (like_string(word), end_page, start_page),
                ).fetchall()
        connection.commit()
        count = connection.execute(
            f""" 
            SELECT COUNT(*) as count FROM bussiness b
            WHERE b.status = "APPROVED"
            AND b.name LIKE ? 
            """,
            (like_string(word),),
        ).fetchone()
        return [res, count["count"]]
    except Exception as error:
        print(error)
        raise Exception(error)


# DONE: Nearest Bussiness
def get_by_nearest(lat, lon, city, start_page, end_page):
    try:
        float(lat)
        float(lon)
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            """
                        
    SELECT b.*, ACOS((SIN(RADIANS(?)) * SIN(RADIANS(b.lat))) + (COS(RADIANS(?)) * COS(RADIANS(b.lat))) * (COS(RADIANS(b.lon) - RADIANS(?)))) * 6371 as distance
    FROM bussiness b
    WHERE city LIKE ?
    AND b.status = "APPROVED"
    ORDER BY distance ASC
    LIMIT ?
    OFFSET ?
     """,
            (lat, lat, lon, like_string(city), end_page, start_page),
        ).fetchall()

        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


# DONE: (Limited) Nearest Bussiness
def get_by_nearest_limited(lat, lon, city):
    try:
        float(lat)
        float(lon)
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            """
SELECT * , RANK() OVER (ORDER BY ( 3959 * acos( cos( radians(?) ) * cos( radians(lat) ) * cos( radians(lon) - radians(?) ) + sin( radians(?) ) * sin( radians(lat) ) ) )  DESC) as rank
FROM bussiness
WHERE city LIKE ?

LIMIT 5""",
            (lat, lon, lat, like_string(city)),
        ).fetchall()

        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


# DONE: Bussiness which have that product
def get_bussiness_has_product(product_id):
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            """
            SELECT b.*, s.price FROM bussiness b
            JOIN stocks s on s.bussiness_id = b.id 
            JOIN products p on s.product_id = p.id
            WHERE p.id = ?
            AND b.status = "APPROVED"
            GROUP BY b.id
            """,
            (product_id,),
        ).fetchall()
        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


# DONE: Recent Added Bussiness
def get_newest(city, start_page, end_page):
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        res = connection.execute(
            """
            SELECT p.*, FROM bussiness b
            WHERE b.city LIKE ?
            ORDER BY b.created_at
            LIMIT ?
            OFFSET ? 
            """,
            (like_string(city), end_page, start_page),
        ).fetchall()
        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


def search_on_bussiness(word, bussiness_id, start_page, end_page):
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
            res = connection.execute(
                f"""
           SELECT p.* FROM products p
           JOIN stocks s on s.product_id = p.id
           JOIN bussiness b on b.id = s.bussiness_id
           WHERE
           p.name LIKE ?
           AND b.id = ?
           AND b.status = "APPROVED"
           GROUP BY p.id
           LIMIT ?
           OFFSET ?
               """,
                (like_string(word), bussiness_id, end_page, start_page),
            ).fetchall()

        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)


def tags_setter(bussiness_id, tags):
    try:
        with sqlite3.connect("database.db") as connection:
            connection.row_factory = dict_factory
        cursor = connection.cursor()
        connection.execute(
            """DELETE FROM tags_bussiness WHERE bussiness_id = ?
            """,
            (bussiness_id,),
        )
        connection.commit()
        tags_data = [(int(tag["id"]), int(bussiness_id)) for tag in tags]
        res = connection.executemany(
            """INSERT INTO tags_bussiness (tag_id, bussiness_id) VALUES (?,?)""",
            tags_data,
        ).fetchall()
        connection.commit()
        return res
    except Exception as error:
        print(error)
        raise Exception(error)
