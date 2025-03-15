from flask import Blueprint, request, render_template, jsonify, session
from flask_login import current_user

from services.bussiness_service import *
from services.products_service import (
    get_newest_by_bussiness as newest_products,
    get_popular_by_bussiness as popular_products,
    get_top_rated_by_bussiness as top_rated_products,
    search_by_bussiness,
)
from services.tags_service import (
    get_all as get_all_tags,
    get_tags_by_bussiness as tags_by_bussiness,
)

from services.brands_service import get_popular_by_bussiness as brands_popular
from services.ratings_service import get_average_by_bussiness as rating_bussiness
from helpers import set_pagination, roles_list, filter_list, type_list

bussiness_bp = Blueprint("bussiness", __name__)

# BASIC DONE


@bussiness_bp.route("/test")
def index():
    return "Hello Bussiness!"


@bussiness_bp.route("/all", methods=["GET"])
def find_all():
    response = get_all()
    print(response)
    return jsonify(response)


@bussiness_bp.route("/", methods=["GET"])
def find():
    id = request.args.get("id")
    response = get(id)
    return jsonify(response)


@bussiness_bp.route("/", methods=["POST"])
def create():
    data = request.get_json()
    data["slug"] = slug_generator(data["name"])
    data["city"] = session["city"]
    data["user_id"] = current_user.get_id() or 3
    response = insert(data)
    tags = tags_setter(response[0]["id"], data["tags"])
    return jsonify(response)


@bussiness_bp.route("/", methods=["PUT"])
def edit():
    id = request.args.get("id")
    data = request.get_json()
    data["slug"] = slug_generator(data["name"])
    data["city"] = session["city"]
    response = update(id, data)
    tags = tags_setter(response[0]["id"], data["tags"])
    return jsonify(response)


@bussiness_bp.route("/", methods=["DELETE"])
def remove():
    id = request.args.get("id")
    response = delete(id)
    return jsonify(response)


@bussiness_bp.route("/", methods=["PATCH"])
def edit_status():
    id = request.args.get("id")
    status = request.get_json()["status"]
    response = update_status(id, status)
    return jsonify(response)


@bussiness_bp.route("/form", methods=["GET"])
def form():
    id = request.args.get("id", None)
    if id:
        bussiness = get(id)
        current_tags = tags_by_bussiness(id)
    else:
        bussiness = None
        current_tags = []
    tags = get_all_tags()
    print(current_tags)
    return render_template(
        "form_create/form_create_bussiness.html",
        tags=tags,
        bussiness=bussiness,
        current_tags=current_tags,
    )


@bussiness_bp.route("/edit/form", methods=["GET"])
def edit_form():
    return render_template("")


# CLIENT


@bussiness_bp.route("/search/<slug>", methods=["GET"])
def find_by_slug(slug):
    lat = session.get("lat", 0)
    lon = session.get("lon", 0)
    bussiness = get_by_slug(slug, lat, lon)
    print(bussiness)
    if not bussiness:
        print("Not found")
        return ValueError("Not found")

    [popular, count] = popular_products("", slug, True)
    [popular_brands, count] = brands_popular(int(bussiness["id"]), True)
    [newest, count] = newest_products("", slug, True)
    [top_discounts, count] = get_most_discount_by_bussiness("", slug, True)
    [top_rated, count] = top_rated_products("", slug, True)
    rating = rating_bussiness(int(bussiness["id"]))

    return render_template(
        "details/details_bussiness.html",
        bussiness=bussiness,
        popular_brands=popular_brands,
        popular_products=popular,
        top_discounts=top_discounts,
        top_rated=top_rated,
        newest=newest,
        rating=rating,
    )


@bussiness_bp.route("<slug>/search/products", methods=["GET"])
def products_by_bussiness(slug):
    # TODO: Implement filtering wtf is wrong
    page = request.args.get("page", None)
    filter = request.args.get("filter", "top_rated")
    order = request.args.get("order", "DESC")
    json_req = request.args.get("json", None)
    word = request.args.get("word", "")
    lat = session.get("lat", 0)
    lon = session.get("lon", 0)
    bussiness = get_by_slug(slug, lat, lon)
    [start_pagination, end_pagination] = set_pagination(page)
    [response, count] = search_by_bussiness(
        slug, word, start_pagination, end_pagination, filter, order
    )
    if not json_req:
        return render_template(
            "search/bussiness_search.html",
            items=response,
            count=count,
            pages=count / 12,
            bussiness=bussiness,
        )
    else:
        return jsonify({"data": response, "count": count})


@bussiness_bp.route("/popular", methods=["GET"])
def find_popular():
    city = request.args.get("city", "")
    page = request.args.get("page", None)
    [start_pagination, end_pagination] = set_pagination(page)
    response = get_popular(city, start_pagination, end_pagination)
    return jsonify(response)  # render_template('', bussiness=response)


@bussiness_bp.route("/discounts", methods=["GET"])
def find_most_discounter():
    city = request.args.get("city", "")
    page = request.args.get("page", None)
    [start_pagination, end_pagination] = set_pagination(page)

    response = get_by_most_discount(city, start_pagination, end_pagination)
    return jsonify(response)  # render_template('', bussiness=response)


@bussiness_bp.route("/nearest", methods=["GET"])
def find_by_nearest():
    lat = request.args.get("lat", 0)
    lon = request.args.get("lon", 0)
    city = request.args.get("city", "")
    page = request.args.get("page", None)
    [start_pagination, end_pagination] = set_pagination(page)
    response = get_by_nearest(lat, lon, city, start_pagination, end_pagination)
    return jsonify(response)  # render_template('', bussiness=response)


@bussiness_bp.route("/top", methods=["GET"])
def find_top_rated():
    city = request.args.get("city")
    page = request.args.get("page", None)
    [start_pagination, end_pagination] = set_pagination(page)

    response = get_top_rated(city, start_pagination, end_pagination)
    return render_template("", bussiness=response)


@bussiness_bp.route("/newest", methods=["GET"])
def find_newest():
    city = request.args.get("city")
    page = request.args.get("page", None)
    [start_pagination, end_pagination] = set_pagination(page)

    response = get_newest(city, start_pagination, end_pagination)
    return render_template("", bussiness=response)


@bussiness_bp.route("/<slug>/<filter>", methods=["GET"])
def find_by_product_filter(slug, filter=filter_list["newest"]):
    if filter not in filter_list:
        return "error"
    page = request.args.get("page", None)
    [start_pagination, end_pagination] = set_pagination(page)
    if filter == filter_list["top_rated"]:
        response = top_rated_products(slug, False, start_pagination, end_pagination)
    elif filter == filter_list["popular"]:
        response = popular_products(slug, False, start_pagination, end_pagination)
    elif filter == filter_list["most_discount"]:
        response = get_most_discount_by_bussiness(
            slug, False, start_pagination, end_pagination
        )
    else:
        response = newest_products(slug, False, start_pagination, end_pagination)
    return render_template("", products=response)


@bussiness_bp.route("/<status>", methods=["GET"])
def get_bussiness_by_status(status):
    if status not in status_list:
        return "error"
    name = request.args.get("name", "")
    page = request.args.get("page", None)
    [start_pagination, end_pagination] = set_pagination(page)
    [response, count] = get_by_status(status, start_pagination, end_pagination, name)
    return jsonify({"data": response, "count": count / 12})


@bussiness_bp.route("/brands/<slug>", methods=["GET"])
def get_brands_by_bussiness(slug):
    page = request.args.get("page", None)
    [start_pagination, end_pagination] = set_pagination(page)
    [response, count] = brands_popular(slug, False, start_pagination, end_pagination)
    return jsonify(response)


# @bussiness_bp.route('/owner', methods=['GET'])
# def find_by_owner():
#     id = request.args.get('id')
#     response = get_by_owner(id)
#     print(response)
#     return 'Hello Bussiness!'


# @bussiness_bp.route('/owner/popular', methods=['GET'])
# def find_popular_by_owner():
#     id = request.args.get('id')
#     response = get_by_owner_popular(id)
#     print(response)
#     return 'Hello Bussiness!'
