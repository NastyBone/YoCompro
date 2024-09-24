from flask import Blueprint, jsonify, request, render_template, abort
from services.products_service import get_by_search_tags as search_product
from services.bussiness_service import get_by_search_tags as bussiness_by_tag
from helpers import to_tag_ids, set_pagination, roles_list
search_bp = Blueprint("search", __name__)


@search_bp.route('/products', methods=['GET'])
def search_products():
    page = request.args.get('page', None)
    data = request.get_json()
    name = request.args.get('name', '')
    [start_pagination, end_pagination] = set_pagination(page)
    tag_ids = to_tag_ids(data.get('tags', []))
    response = search_product(name, tag_ids, start_pagination, end_pagination)
    return jsonify(response)
    # return render_template('', products=response)


@search_bp.route('/bussiness', methods=['GET'])
def search_bussiness():
    page = request.args.get('page')
    data = request.get_json()
    name = request.args.get('name', '')
    [start_pagination, end_pagination] = set_pagination(page)
    tag_ids = to_tag_ids(data.get('tags', []))
    response = bussiness_by_tag(
        name, tag_ids, start_pagination, end_pagination)
    return jsonify(response)
    # return render_template('', bussiness=response)
