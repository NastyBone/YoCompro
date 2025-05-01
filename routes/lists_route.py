from flask import Blueprint, render_template, request, jsonify
from services.lists_services import *
from guard import *

lists_bp = Blueprint("lists", __name__)


@lists_bp.route("/test")
def index():
    return "Hello Lists!"


@lists_bp.route("/", methods=["GET"])
def find():
    id = request.args.get("id")
    response = get(id)
    return jsonify(response)


@lists_bp.route("/all", methods=["GET"])
def find_all():
    response = get_all()
    return jsonify(response)


@lists_bp.route("/", methods=["POST"])
def create():
    data = request.get_json()
    response = insert(data)
    return jsonify(response)


# @lists_bp.route('/', methods=['PUT'])
# def edit():
#     id = request.args.get('id')
#     data = request.get_json()
#     response = update(id, data)
#     print(response)
#     return 'Hello Lists!'


@lists_bp.route("/", methods=["DELETE"])
@secure_access()
def remove():
    id = request.args.get("id")
    response = delete(id)
    return jsonify(response)


@lists_bp.route("/add", methods=["POST"])
@secure_access()
def add_product():
    list_by_user = get_id_by_user(current_user.get_id())
    id = list_by_user[0].get("list_id")
    stock_id = request.args.get("stock_id")
    print(stock_id, id)
    response = insert_product(id, stock_id)
    print(response)
    return jsonify(response)


@lists_bp.route("/remove", methods=["POST"])
@secure_access()
def remove_product():
    list_by_user = get_id_by_user(current_user.get_id())
    id = list_by_user[0].get("list_id")
    stock_id = request.args.get("stock_id")
    response = delete_product(id, stock_id)
    return jsonify(response)


@lists_bp.route("/user", methods=["GET"])
@secure_access()
def find_by_user():
    id = current_user.get_id()
    [response, count] = get_by_user(id)
    return render_template(
        "lists/list.html", list=response, count=count, pages=count / 12
    )
