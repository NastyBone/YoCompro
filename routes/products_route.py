from flask import Blueprint, request, jsonify, render_template, session
from services.products_service import *
from classes.product_class import *
from services.brands_service import (
    get_by_product_id as brand_by_product,
    get_all as get_all_brands,
)
from services.ratings_service import get_average_by_product as rating_by_product
from services.bussiness_service import (
    get_bussiness_has_product_by_distance,
    get_bussiness_has_product_by_price,
    search_by_products,
)
from helpers import roles_list, set_pagination, filter_list
from services.tags_service import get_all as get_all_tags

products_bp = Blueprint("products", __name__)

# BASIC


@products_bp.route("/test", methods=["GET"])
def index():
    return "Hello Products!"


@products_bp.route("/all", methods=["GET"])
def find_all():
    response = get_all()
    print(response)
    return jsonify(response)


@products_bp.route("/", methods=["GET"])
def find():
    id = request.args.get("id")
    response = get(id)
    print(response)
    return jsonify(response)


@products_bp.route("/", methods=["POST"])
def create():
    data = request.get_json()
    data["slug"] = slug_generator(data["name"])
    response = insert(data)
    tags = tags_setter(response[0]["id"], data["tags"])
    return jsonify(response)


@products_bp.route("/", methods=["PUT"])
def edit():
    id = request.args.get("id")
    data = request.get_json()
    response = update(id, data)
    tags = tags_setter(response[0]["id"], data["tags"])
    return jsonify(response)


@products_bp.route("/", methods=["DELETE"])
def remove():
    id = request.args.get("id")
    response = delete(id)
    return jsonify(response)


@products_bp.route("/", methods=["PATCH"])
def edit_status():
    id = request.args.get("id")
    status = request.get_json()["status"]
    response = update_status(id, status)
    return "Hello Products!"


@products_bp.route("/create/form", methods=["GET"])
def create_form():
    brands = get_all_brands()
    tags = get_all_tags()
    return render_template(
        "form_create/form_create_product.html", brands=brands, tags=tags
    )


@products_bp.route("/edit/form", methods=["GET"])
def edit_form():
    return render_template("")


# CLIENT


@products_bp.route("/search/<slug>", methods=["GET"])
def find_by_slug(slug):
    lat = session.get("lat", None)
    lon = session.get("lon", None)
    product = get_by_slug(slug)
    [bussiness_by_distance, count] = get_bussiness_has_product_by_distance(
        int(product["id"]), lat, lon, True
    )
    [bussiness_by_price, count] = get_bussiness_has_product_by_price(
        int(product["id"]), True
    )
    brand = brand_by_product(int(product["id"]))[0]
    rating = rating_by_product(int(product["id"]))[0]

    # return render_template('',
    #                        product=product,
    #                        brand=brand,
    #                        rating=rating,
    #                        bussiness=bussiness)
    return render_template(
        "details/detail_product.html",
        product=product,
        brand=brand,
        rating=rating,
        bussiness_by_distance=bussiness_by_distance,
        bussiness_by_price=bussiness_by_price,
    )


@products_bp.route("/popular", methods=["GET"])
def find_popular():
    city = request.args.get("city", "")
    page = request.args.get("page", None)
    [start_pagination, end_pagination] = set_pagination(page)
    response = get_popular(city, start_pagination, end_pagination)
    return jsonify(response)
    # return render_template('', products=response)


@products_bp.route("/newest", methods=["GET"])
def find_newest():
    city = request.args.get("city")
    page = request.args.get("page", None)
    [start_pagination, end_pagination] = set_pagination(page)
    response = get_newest(city, start_pagination, end_pagination)
    return jsonify(response)


@products_bp.route("/top_rated", methods=["GET"])
def find_top():
    city = request.args.get("city", "")
    page = request.args.get("page", None)
    [start_pagination, end_pagination] = set_pagination(page)

    response = get_top_rated(city, start_pagination, end_pagination)
    # return render_template('', products=response)
    return jsonify(response)


@products_bp.route("/discounts", methods=["GET"])
def find_by_discount():
    id = request.args.get("id")
    response = get_by_discounts(id)
    return jsonify(response)


@products_bp.route("/discounts/all", methods=["GET"])
def find_all_by_discount():
    city = request.args.get("city", "")
    response = get_all_by_discounts(city)
    return jsonify(response)


@products_bp.route("/<status>", methods=["GET"])
def get_products_by_status(status):
    if status not in status_list:
        return "error"
    name = request.args.get("name", "")
    page = request.args.get("page", None)
    [start_pagination, end_pagination] = set_pagination(page)
    [response, count] = get_by_status(status, start_pagination, end_pagination, name)
    return jsonify({"data": response, "count": count / 12})


@products_bp.route("<slug>/search/bussiness", methods=["GET"])
def bussiness_by_products(slug):
    print("is here??")
    lat = session.get("lat", None)
    lon = session.get("lon", None)
    page = request.args.get("page", None)
    json_req = request.args.get("json", None)
    filter = request.args.get("filter", "cheapest")
    order = request.args.get("order", "DESC")
    word = request.args.get("word", "")
    [start_pagination, end_pagination] = set_pagination(page)
    product = get_by_slug(slug)
    [response, count] = search_by_products(
        slug, word, lat, lon, start_pagination, end_pagination, filter, order
    )
    if not json_req:
        return render_template(
            "search/product_search.html",
            items=response,
            product=product,
            count=count,
            pages=count / 12,
        )
    else:
        return jsonify({"data": response, "count": count / 12})


@products_bp.route("/<slug>/<filter>", methods=["GET"])
def find_by_bussiness_filter(slug, filter=filter_list["newest"]):
    lat = session.get("lat", None)
    lon = session.get("lon", None)
    page = request.args.get("page", None)
    [start_pagination, end_pagination] = set_pagination(page)
    product = get_by_slug(slug)
    if filter == "nearest":
        response = get_bussiness_has_product_by_distance(
            product_id=product["id"],
            lat=lat,
            lon=lon,
            start_page=start_pagination,
            end_page=end_pagination,
        )
    elif filter == "cheapest":
        response = get_bussiness_has_product_by_price(
            product_id=product["id"],
            start_page=start_pagination,
            end_page=end_pagination,
        )
    return jsonify(response)


# DESCARTADO
# @products_bp.route('/nearest', methods=['GET'])
# def find_by_nearest():
#     data = request.get_json()
#     response = get_by_brand(data['brand_id'])
#     return jsonify(response)
