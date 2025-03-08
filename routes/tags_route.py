from flask import Blueprint, render_template, request, jsonify
from services.tags_service import *
from helpers import set_pagination

tags_bp = Blueprint("tags", __name__)


@tags_bp.route("/all", methods=["GET"])
def find_all():
    response = get_all()
    return jsonify(response)


@tags_bp.route("/", methods=["GET"])
def find():
    id = request.args.get("id")
    response = get(id)
    return jsonify(response)


@tags_bp.route("/", methods=["POST"])
def create():
    data = request.get_json()
    response = insert(data)
    return jsonify(response)


@tags_bp.route("/", methods=["PUT"])
def edit():
    data = request.get_json()
    id = request.args.get("id")
    response = update(id, data)
    print(response)
    return jsonify(response)


@tags_bp.route("/", methods=["DELETE"])
def remove():
    id = request.args.get("id")
    response = delete(id)
    print(response)
    return jsonify(response)


@tags_bp.route("/", methods=["PATCH"])
def edit_status():
    id = request.args.get("id")
    status = request.get_json()["status"]
    response = update_status(id, status)
    print(response)
    return jsonify(response)


@tags_bp.route("/<status>", methods=["GET"])
def get_tags_by_status(status):
    if status not in status_list:
        return "error"
    word = request.args.get("word", "")
    page = request.args.get("page", None)
    [start_pagination, end_pagination] = set_pagination(page)
    [response, count] = get_by_status(status, start_pagination, end_pagination, word)
    return jsonify({"data": response, "count": count / 12})


@tags_bp.route("/create/form", methods=["GET"])
def create_form():
    return render_template("form_create/form_create_tag.html")


@tags_bp.route("/edit/form", methods=["GET"])
def edit_form():
    return render_template("")


@tags_bp.route("/test", methods=["GET"])
def index():
    return "Hello Tags!"
