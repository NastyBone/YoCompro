from flask import Blueprint, request, jsonify, render_template
from services.products_service import *
from classes.product_class import *
from services.brands_service import get_by_product_id as brand_by_product
from services.ratings_service import get_average_by_product as rating_by_product
from services.bussiness_service import get_bussiness_has_product
from helpers import roles_list, set_pagination

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
    return render_template("")


@products_bp.route("/edit/form", methods=["GET"])
def edit_form():
    return render_template("")


# CLIENT


@products_bp.route("/search/<slug>", methods=["GET"])
def find_by_slug(slug):
    product = get_by_slug(slug)[0]
    print("***************************", product)
    bussiness = get_bussiness_has_product(int(product["id"]))
    brand = brand_by_product(int(product["id"]))[0]
    rating = rating_by_product(int(product["id"]))[0]

    # return render_template('',
    #                        product=product,
    #                        brand=brand,
    #                        rating=rating,
    #                        bussiness=bussiness)
    return jsonify(
        {"product": product, "bussiness": bussiness, "brand": brand, "rating": rating}
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


# DESCARTADO
# @products_bp.route('/nearest', methods=['GET'])
# def find_by_nearest():
#     data = request.get_json()
#     response = get_by_brand(data['brand_id'])
#     return jsonify(response)
