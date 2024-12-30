from unidecode import unidecode

status_list = {"approved": "APPROVED", "in_review": "IN REVIEW", "rejected": "REJECTED"}
roles_list = {"client": "CLIENT", "owner": "OWNER", "admin": "ADMIN"}
filter_list = {
    "top_rated": "TOP_RATED",
    "newest": "NEWEST",
    "popular": "POPULAR",
    "nearest": "NEAREST",
    "most_discount": "MOST_DISCOUNT",
    "cheapest": "CHEAPEST",
}
type_list = {"brand": "BRAND", "bussiness": "BUSSINESS"}


def to_tag_ids(tags):
    tags_ids = [tag["id"] for tag in tags]
    return tags_ids


def slug_builder(name):
    return name.strip().lower().replace(" ", "-")


def set_pagination(page: str | None = None, perPage: int | None = 12):
    if page == None or page == 1:
        start_pagination = 0
        end_pagination = perPage
    else:
        start_pagination = (int(page) - 1) * perPage
        end_pagination = start_pagination + perPage
    return [start_pagination, end_pagination]


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def like_string(string):
    return "%" + str(string) + "%"


def limit_or_pagination(limited, start_page, end_page):
    if (start_page != None and end_page != None) and not (
        isinstance(start_page, int) and isinstance(end_page, int)
    ):
        raise ValueError("start_page and end_page must be integers.")
    limited_clause = "LIMIT 5" if limited else ""
    pagination_clause = (
        f"LIMIT {int(end_page)} OFFSET {start_page}"
        if start_page is not None and end_page is not None
        else ""
    )
    return f"{limited_clause} {pagination_clause}"
