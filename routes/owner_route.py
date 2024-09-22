from flask import Blueprint, request, render_template, redirect, jsonify
from guard import *
from flask_login import current_user
from helpers import roles_list, set_pagination
from services.products_service import get_popular_by_owner as products_popular, get_top_rated_by_owner as products_top_rated
from services.brands_service import *
from services.bussiness_service import get_by_owner_popular as bussiness_popular, get_by_owner as bussiness_all, get_by_owner_top_rated as bussiness_top_rated
from services.stocks_service import get_by_bussiness as stock_bussiness
owner_bp = Blueprint("owner", __name__)


@owner_bp.route('/dashboard', methods=['GET'])
def main():
    owner = current_user.get_id()
    popular_products = products_popular(owner, limited=True)
    popular_bussiness = bussiness_popular(owner, limited=True)
    unpopular_bussiness = bussiness_popular(owner, limited=True, order='ASC')
    return jsonify({"pop_products": popular_products, "pop_bussiness": popular_bussiness, "unpop_bussiness": unpopular_bussiness})
    # return render_template('',
    #                        popular_products=popular_products, popular_bussiness=popular_bussiness,
    #                        unpopular_bussiness=unpopular_bussiness)


@owner_bp.route('/all', methods=['GET'])
def all():
    page = request.args.get('page', None)
    owner = current_user.get_id()
    [start_pagination, end_pagination] = set_pagination(page)
    response = bussiness_all(owner, start_pagination, end_pagination)
    return jsonify(response)
    # return render_template('', bussiness=response)


@owner_bp.route('/bussiness/popular', methods=['GET'])
def popular_bussiness():
    page = request.args.get('page', None)
    owner = current_user.get_id()
    [start_pagination, end_pagination] = set_pagination(page)
    response = bussiness_popular(
        owner, start_page=start_pagination, end_page=end_pagination, order='ASC')
    return jsonify(response)
    # return render_template('', bussiness=response)


@owner_bp.route('/bussiness/unpopular', methods=['GET'])
def unpopular_bussiness():
    page = request.args.get('page', None)
    owner = current_user.get_id()
    [start_pagination, end_pagination] = set_pagination(page)
    response = bussiness_popular(
        owner, start_page=start_pagination, end_page=end_pagination)
    return jsonify(response)
    # return render_template('', bussiness=response)


@owner_bp.route('/products/popular', methods=['GET'])
def popular_products():
    page = request.args.get('page', None)
    owner = current_user.get_id()
    [start_pagination, end_pagination] = set_pagination(page)
    response = products_popular(
        owner, start_page=start_pagination, end_page=end_pagination)
    return jsonify(response)
    # return render_template('', products=response)


@owner_bp.route('/bussiness/less_rated', methods=['GET'])
def less_rated_bussiness():
    page = request.args.get('page', None)
    owner = current_user.get_id()
    [start_pagination, end_pagination] = set_pagination(page)
    response = bussiness_top_rated(
        owner, start_page=start_pagination, end_page=end_pagination, order='ASC')
    return jsonify(response)
    # return render_template('', products=response)


@owner_bp.route('/bussiness/top_rated', methods=['GET'])
def top_rated_bussiness():
    page = request.args.get('page', None)
    owner = current_user.get_id()
    [start_pagination, end_pagination] = set_pagination(page)
    response = bussiness_top_rated(
        owner, start_page=start_pagination, end_page=end_pagination)
    return jsonify(response)
    # return render_template('', products=response)


@owner_bp.route('/products/top_rated', methods=['GET'])
def top_rated_products():
    page = request.args.get('page', None)
    owner = current_user.get_id()
    [start_pagination, end_pagination] = set_pagination(page)
    response = products_top_rated(
        owner, start_page=start_pagination, end_page=end_pagination)
    return jsonify(response)
    # return render_template('', products=response)


@owner_bp.route('/products/less_rated', methods=['GET'])
def less_rated_products():
    page = request.args.get('page', None)
    owner = current_user.get_id()
    [start_pagination, end_pagination] = set_pagination(page)
    response = products_top_rated(
        owner, start_page=start_pagination, end_page=end_pagination,    order='ASC')
    return jsonify(response)
    # return render_template('', products=response)


@owner_bp.route('/products/unpopular', methods=['GET'])
def unpopular_products():
    page = request.args.get('page', None)
    owner = current_user.get_id()
    [start_pagination, end_pagination] = set_pagination(page)
    response = products_popular(
        owner, start_page=start_pagination, end_page=end_pagination, order='ASC')
    return jsonify(response)
    # return render_template('', products=response)


@owner_bp.route('/<slug>/stocks', methods=['GET'])
def stocks(slug):
    owner = current_user.get_id()
    page = request.args.get('page', None)
    [start_pagination, end_pagination] = set_pagination(page)
    response = stock_bussiness(slug, owner, start_pagination, end_pagination)
    return jsonify(response)
    # return render_template('', stocks=response)
