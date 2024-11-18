from flask import Blueprint, request, jsonify, render_template
from services.brands_service import *
from helpers import filter_list, roles_list, type_list, set_pagination
from services.products_service import (
    get_popular_by_brand as products_popular,
    get_newest_by_brand as produscts_newest,
    get_top_rated_by_brand as products_top_rated,
)
from services.bussiness_service import get_popular_by_brand as bussiness_popular

brands_bp = Blueprint("brands", __name__)

# BASIC DONE


@brands_bp.route("/test")
def index():
    return "Hello Brands!"


@brands_bp.route("/", methods=["GET"])
def find():
    id = request.args.get("id")
    response = get(id)
    return jsonify(response)


@brands_bp.route("/all", methods=["GET"])
def find_all():
    response = get_all()
    return jsonify(response)


@brands_bp.route("/", methods=["POST"])
def create():
    data = request.get_json()
    response = insert(data)
    return jsonify(response)


@brands_bp.route("/", methods=["PUT"])
def edit():
    id = request.args.get("id")
    data = request.get_json()
    response = update(id, data)
    return jsonify(response)


@brands_bp.route("/", methods=["DELETE"])
def remove():
    id = request.args.get("id")
    response = delete(id)
    return jsonify(response)


@brands_bp.route("/", methods=["PATCH"])
def edit_status():
    status = request.get_json()["status"]
    id = request.args.get("id")
    response = update_status(id, status)
    return jsonify(response)


@brands_bp.route("/create/form", methods=["GET"])
def create_form():
    return render_template("")


@brands_bp.route("/edit/form", methods=["GET"])
def edit_form():
    return render_template("")


#################################################


@brands_bp.route("/<slug>/bussiness/")
def popular_bussines(slug=None):
    city = request.args.get("city", None)
    page = request.args.get("page", None)
    [start_pagination, end_pagination] = set_pagination(page)
    response = bussiness_popular(city, slug, start_pagination, end_pagination)
    return response


@brands_bp.route("/<slug>/products/<filter>", methods=["GET"])
def find_by_product_filter(slug, filter=filter_list["newest"]):
    if filter not in filter_list:
        return "error"
    page = request.args.get("page", None)
    [start_pagination, end_pagination] = set_pagination(page)
    if filter == "top_rated":
        response = products_top_rated(slug, start_pagination, end_pagination)
    elif filter == "popular":
        response = products_popular(slug, start_pagination, end_pagination)
    else:
        response = produscts_newest(slug, start_pagination, end_pagination)
    return jsonify(response)  # render_template('', products=response)
