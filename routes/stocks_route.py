from flask import Blueprint, request, render_template, jsonify
from services.stocks_service import *
from helpers import set_pagination
from guard import secure_access

stocks_bp = Blueprint("stocks", __name__)


@stocks_bp.route('/test', methods=['GET'])
def index():
    return 'Hello Stocks!'


@stocks_bp.route('/all', methods=['GET'])
def find_all():
    response = get_all()
    return jsonify(response)


@stocks_bp.route('/', methods=['GET'])
def find():
    id = request.args.get('id')
    response = get(id)
    return jsonify(response)


@stocks_bp.route('/', methods=['POST'])
def create():
    data = request.get_json()
    response = insert(data)
    return jsonify(response)


@stocks_bp.route('/', methods=['PUT'])
def edit():
    data = request.get_json()
    id = request.args.get('id')
    response = update(id, data)
    return jsonify(response)


@stocks_bp.route('/', methods=['DELETE'])
def remove():
    id = request.args.get('id')
    response = delete(id)
    return jsonify(response)


@stocks_bp.route('/create/form', methods=['GET'])
def create_form():
    return render_template('')


@stocks_bp.route('/edit/form', methods=['GET'])
def edit_form():
    return render_template('')

#################################


@stocks_bp.route('/bussiness', methods=['GET'])
@secure_access()
def find_by_bussiness():
    owner_id = request.args.get('owner_id')
    bussiness_id = request.args.get('bussiness_id')
    page = request.args.get('page', None)
    [start_pagination, end_pagination] = set_pagination(page)
    response = get_by_bussiness(
        bussiness_id, owner_id, start_pagination, end_pagination)
    return jsonify(response)
