from flask import Blueprint, request, jsonify
from services.lists_services import *
from guard import *

lists_bp = Blueprint("lists", __name__)


@lists_bp.route('/test')
def index():
    return 'Hello Lists!'


@lists_bp.route('/', methods=['GET'])
def find():
    id = request.args.get('id')
    response = get(id)
    return jsonify(response)


@lists_bp.route('/all', methods=['GET'])
def find_all():
    response = get_all()
    return jsonify(response)


@lists_bp.route('/', methods=['POST'])
def create():
    data = request.get_json()
    print(data)
    response = insert(data)
    return jsonify(response)


# @lists_bp.route('/', methods=['PUT'])
# def edit():
#     id = request.args.get('id')
#     data = request.get_json()
#     response = update(id, data)
#     print(response)
#     return 'Hello Lists!'


@lists_bp.route('/', methods=['DELETE'])
def remove():
    id = request.args.get('id')
    response = delete(id)
    return jsonify(response)


@lists_bp.route('/add', methods=['POST'])
def add_product():
    id = request.args.get('id')
    stock_id = request.args.get('stock_id')
    response = insert_product(id, stock_id)
    return jsonify(response)


@lists_bp.route('/remove', methods=['POST'])
def remove_product():
    id = request.args.get('id')
    stock_id = request.args.get('stock_id')
    response = delete_product(id, stock_id)
    return jsonify(response)


@lists_bp.route('/user', methods=['GET'])
# @secure_access()
def find_by_user():
    id = request.args.get('user_id')
    response = get_by_user(id)
    return jsonify(response)
