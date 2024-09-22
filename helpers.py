status_list = {'approved': 'APPROVED',
               'in_review': 'IN REVIEW', 'rejected': 'REJECTED'}
roles_list = {'client': 'CLIENT', 'owner': 'OWNER', 'admin': 'ADMIN'}
filter_list = {'top_rated': 'TOP_RATED',
               'newest': 'NEWEST', 'popular': 'POPULAR'}
type_list = {'brand': 'BRAND', 'bussiness': 'BUSSINESS'}


def to_tag_ids(tags):
    tags_ids = [tag['id'] for tag in tags]
    return tags_ids


def slug_builder():
    return ''


def set_pagination(page: str | None = None):
    if (page == None):
        start_pagination = 0
        end_pagination = 10
    else:
        start_pagination = (int(page, 10) - 1) * 10
        end_pagination = (start_pagination + 10)
    return [start_pagination, end_pagination]


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def like_string(string):
    return "%" + string + "%"
