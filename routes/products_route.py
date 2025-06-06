from flask import Blueprint, json, request, jsonify, render_template, session
from flask_login import current_user
from guard import role_required
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
from helpers import generate_filename, roles_list, set_pagination, filter_list
from services.tags_service import (
    get_all as get_all_tags,
    get_tags_by_products as tags_by_products,
)
from services.images_service import insert as insert_image, update as update_image

products_bp = Blueprint("products", __name__)

# BASIC


@products_bp.route("/test", methods=["GET"])
def index():
    return "Hello Products!"


@products_bp.route("/all", methods=["GET"])
def find_all():
    response = get_all()
    return jsonify(response)


@products_bp.route("/", methods=["GET"])
def find():
    id = request.args.get("id")
    response = get(id)
    return jsonify(response)


@products_bp.route("/", methods=["POST"])
def create():
    data = request.form
    image = request.files.get("image")
    image_name = generate_filename(image.filename)
    response = insert(
        {
            "name": data.get("name"),
            "slug": slug_generator(data.get("name")),
            "brand_id": data.get("brand_id"),
            "description": data.get("description"),
        }
    )
    path = f"static/images/brands/{image_name}"
    image.save(path)
    insert_image(
        image_name, response[0]["id"], "/" + path, "images_products", "product_id"
    )
    tags = tags_setter(response[0]["id"], data.get("tags"))
    return jsonify(response)


@products_bp.route("/", methods=["PUT"])
@role_required("ADMIN")
def edit():
    id = request.args.get("id")
    data = request.form
    response = update(
        id,
        {
            "name": data.get("name"),
            "slug": slug_generator(data.get("name")),
            "brand_id": data.get("brand_id"),
            "description": data.get("description"),
        },
    )
    image = request.files.get("image")
    if image:
        image_name = generate_filename(image.filename)
        path = f"static/images/products/{image_name}"
        image.save(path)
        update_image(
            image_name,
            response[0]["id"],
            "/" + path,
            "images_products",
            "product_id",
        )
    tags = tags_setter(response[0]["id"], data.get("tags"))
    return jsonify(response)


@products_bp.route("/", methods=["DELETE"])
def remove():
    id = request.args.get("id")
    response = delete(id)
    return "Success!"


@products_bp.route("/", methods=["PATCH"])
def edit_status():
    id = request.args.get("id")
    status = request.get_json()["status"]
    response = update_status(id, status)
    return "Success"


@products_bp.route("/form", methods=["GET"])
def form():
    id = request.args.get("id", None)
    if id:
        product = get(id)
        current_tags = tags_by_products(id)
    else:
        product = [None]
        current_tags = []
    brands = get_all_brands()
    tags = get_all_tags()
    return render_template(
        "form_create/form_create_product.html",
        brands=brands,
        tags=tags,
        product=product,
        current_tags=current_tags,
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
        slug,
        word,
        lat,
        lon,
        current_user.get_id(),
        start_pagination,
        end_pagination,
        filter,
        order,
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
    json_req = request.args.get("json", None)
    page = request.args.get("page", None)
    user_id = current_user.get_id()
    [start_pagination, end_pagination] = set_pagination(page)
    product = get_by_slug(slug)
    if filter == "nearest":
        [response, count] = get_bussiness_has_product_by_distance(
            product_id=product["id"],
            user_id=user_id,
            lat=lat,
            lon=lon,
            start_page=start_pagination,
            end_page=end_pagination,
        )
    elif filter == "cheapest":
        [response, count] = get_bussiness_has_product_by_price(
            product_id=product["id"],
            user_id=user_id,
            start_page=start_pagination,
            end_page=end_pagination,
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


# DESCARTADO
# @products_bp.route('/nearest', methods=['GET'])
# def find_by_nearest():
#     data = request.get_json()
#     response = get_by_brand(data['brand_id'])
#     return jsonify(response)
