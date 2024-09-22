from flask import Blueprint, request, jsonify
from services.tags_service import *
tags_bp = Blueprint("tags", __name__)


@tags_bp.route('/all', methods=['GET'])
def find_all():
    response = get_all()
    return jsonify(response)


@tags_bp.route('/', methods=['GET'])
def find():
    id = request.args.get('id')
    response = get(id)
    return jsonify(response)


@tags_bp.route('/', methods=['POST'])
def create():
    data = request.get_json()
    response = insert(data)
    return jsonify(response)


@tags_bp.route('/', methods=['PUT'])
def edit():
    data = request.get_json()
    id = request.args.get('id')
    response = update(id, data)
    print(response)
    return jsonify(response)


@tags_bp.route('/', methods=['DELETE'])
def remove():
    id = request.args.get('id')
    response = delete(id)
    print(response)
    return jsonify(response)


@tags_bp.route('/', methods=['PATCH'])
def edit_status():
    id = request.args.get('id')
    status = request.get_json()['status']
    response = update_status(id, status)
    print(response)
    return jsonify(response)


@tags_bp.route('/test', methods=['GET'])
def index():
    return 'Hello Tags!'
