from flask import Blueprint, request, jsonify
from flask_login import current_user
from services.ratings_service import *
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
    product_id = data.get("product_id", None)
    bussiness_id = data.get("bussiness_id", None)
    user_id = 1  # current_user.get_id()
    if not user_id:
        return jsonify({"error": "User not found"}), 404
    response = insert_rating(user_id, bussiness_id, product_id, score)
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


@ratings_bp.route("/bussiness", methods=["GET"])
def find_by_bussiness():
    id = request.args.get("id")
    page = request.args.get("page", None)
    [start_pagination, end_pagination] = set_pagination(page)
    response = get_by_bussiness(id, start_pagination, end_pagination)
    return jsonify(response)


@ratings_bp.route("/product", methods=["GET"])
def find_by_product():
    id = request.args.get("id")
    page = request.args.get("page", None)
    [start_pagination, end_pagination] = set_pagination(page)
    response = get_by_product(id, start_pagination, end_pagination)
    return jsonify(response)


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
