from flask import Blueprint, render_template, request, jsonify
from flask_login import current_user
from services.ratings_service import *
from services.bussiness_service import get_by_slug as get_bussiness
from services.products_service import get_by_slug as get_product
from helpers import set_pagination
from guard import secure_access

ratings_bp = Blueprint("ratings", __name__)


@ratings_bp.route("/", methods=["GET"])
def find():
    id = request.args.get("id")
    response = get(id)
    return jsonify(response)


@ratings_bp.route("/all", methods=["GET"])
def find_all():
    response = get_all()
    return jsonify(response)


@ratings_bp.route("/", methods=["POST"])
# @secure_access()
def create():
    data = request.get_json()
    score = data.get("score", None)
    comment = data.get("comment", None)
    product_id = data.get("product_id", None)
    bussiness_id = data.get("bussiness_id", None)
    user_id = 3  # current_user.get_id()
    if not user_id:
        return jsonify({"error": "User not found"}), 404
    response = insert_rating(user_id, bussiness_id, product_id, score, comment)
    return jsonify(response)


# @ratings_bp.route('/', methods=['PUT'])
# @secure_access()
# def edit():
#     id = request.args.get('id')
#     data = request.get_json()
#     response = update(id, data)
#     return jsonify(response)


@ratings_bp.route("/", methods=["DELETE"])
@secure_access()
def remove():
    id = request.args.get("id")
    response = delete(id)
    return jsonify(response)


@ratings_bp.route("/user", methods=["GET"])
@secure_access()
def find_by_user():
    user_id = current_user.get_id()
    response = get_by_user(user_id)
    return jsonify(response)


@ratings_bp.route("/bussiness/<slug>", methods=["GET"])
def find_by_bussiness(slug):
    page = request.args.get("page", None)
    [start_pagination, end_pagination] = set_pagination(page)
    bussiness = get_bussiness(slug)
    [response, count] = get_by_bussiness(
        int(bussiness["id"]), False, start_pagination, end_pagination
    )
    return render_template(
        "ratings/ratings_bussiness.html",
        ratings=response,
        bussiness=bussiness,
        count=count,
        pages=count / 12,
    )


@ratings_bp.route("/product/<slug>", methods=["GET"])
def find_by_product(slug):
    page = request.args.get("page", None)
    [start_pagination, end_pagination] = set_pagination(page)
    product = get_product(slug)
    [response, count] = get_by_product(
        int(product["id"]), False, start_pagination, end_pagination
    )
    return render_template(
        "ratings/ratings_products.html",
        ratings=response,
        product=product,
        count=count,
        pages=count / 12,
    )


@ratings_bp.route("/<type>/<id>/aux", methods=["GET"])
def find_auxiliar(type, id):
    score = request.args.get("score")
    time = request.args.get("time")
    if score not in ["ASC", "DESC"]:
        ValueError("Undefined type")
    if time not in ["ASC", "DESC"]:
        ValueError("Undefined Filter")
    page = request.args.get("page")
    [start_pagination, end_pagination] = set_pagination(page)

    if type == "bussiness":
        [response, count] = get_by_bussiness(
            id, False, start_pagination, end_pagination, score, time
        )
    elif type == "products":
        [response, count] = get_by_product(
            id, False, start_pagination, end_pagination, score, time
        )
    else:
        ValueError("Type not valid")
    return jsonify({"data": response, "count": count / 12})  # 12 per page


# DESUSO


@ratings_bp.route("/bussiness/average", methods=["GET"])
def find_avg_by_bussiness():
    id = request.args.get("id")
    response = get_average_by_bussiness(id)
    return jsonify(response)


@ratings_bp.route("/product/average", methods=["GET"])
def find_avg_by_product():
    id = request.args.get("id")
    response = get_average_by_product(id)
    return jsonify(response)


@ratings_bp.route("/test", methods=["GET"])
def index():
    return "Hello Ratings!"
