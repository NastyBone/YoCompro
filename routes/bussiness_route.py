from flask import Blueprint, request, render_template, jsonify
from services.bussiness_service import *
from services.products_service import get_popular_by_bussiness_limited as products_popular_limited, get_newest_by_bussiness as newest_products, get_popular_by_bussiness as popular_products, get_top_rated_by_bussiness as top_rated_products
from services.brands_service import get_popular_by_bussiness as brands_popular
from services.ratings_service import get_average_by_bussiness as rating_bussiness
from helpers import set_pagination, roles_list, filter_list, type_list
bussiness_bp = Blueprint("bussiness", __name__)

# BASIC DONE


@bussiness_bp.route('/test')
def index():
    return 'Hello Bussiness!'


@bussiness_bp.route('/all', methods=['GET'])
def find_all():
    response = get_all()
    print(response)
    return jsonify(response)


@bussiness_bp.route('/', methods=['GET'])
def find():
    id = request.args.get('id')
    response = get(id)
    return jsonify(response)


@bussiness_bp.route('/', methods=['POST'])
def create():
    data = request.get_json()
    response = insert(data)
    tags = tags_setter(response[0]["id"], data['tags'])
    return jsonify(response)


@bussiness_bp.route('/', methods=['PUT'])
def edit():
    id = request.args.get('id')
    data = request.get_json()
    response = update(id, data)
    tags = tags_setter(response[0]["id"], data['tags'])
    return jsonify(response)


@bussiness_bp.route('/', methods=['DELETE'])
def remove():
    id = request.args.get('id')
    response = delete(id)
    return jsonify(response)


@bussiness_bp.route('/', methods=['PATCH'])
def edit_status():
    id = request.args.get('id')
    status = request.get_json()['status']
    response = update_status(id, status)
    return jsonify(response)


@bussiness_bp.route('/create/form', methods=['GET'])
def create_form():
    return render_template('')


@bussiness_bp.route('/edit/form', methods=['GET'])
def edit_form():
    return render_template('')
# CLIENT


@bussiness_bp.route('/search/<slug>', methods=['GET'])
def find_by_slug(slug):
    print(slug)
    bussiness = get_by_slug(slug)
    if not bussiness:
        print('Not found')
        ValueError('Not found')

    popular_products = products_popular_limited(int(bussiness['id']))
    popular_brands = brands_popular(int(bussiness['id']))
    top_discounts = get_most_discount_by_bussiness(int(bussiness['id']))
    rating = rating_bussiness(int(bussiness['id']))
    return jsonify({
        "bussiness": bussiness,
        "popular_products": popular_products,
        "popular_brands": popular_brands,
        "top_discounts": top_discounts,
        "rating": rating
    })  # render_template('', bussiness=bussiness, popular_brands=popular_brands, popular_products=popular_products, top_discounts=top_discounts, rating=rating)


@bussiness_bp.route('/search/product/<slug>', methods=['GET'])
def find_by_slug_product(slug):
    bussiness_id = request.args.get('bussiness_id')
    page = request.args.get('page', None)
    [start_pagination, end_pagination] = set_pagination(page)
    products = search_on_bussiness(
        slug, bussiness_id, start_pagination, end_pagination)
    return jsonify(products)


@bussiness_bp.route('/popular', methods=['GET'])
def find_popular():
    city = request.args.get('city', "")
    page = request.args.get('page', None)
    [start_pagination, end_pagination] = set_pagination(page)
    response = get_popular(city, start_pagination, end_pagination)
    return jsonify(response)  # render_template('', bussiness=response)


@bussiness_bp.route('/discounts', methods=['GET'])
def find_most_discounter():
    city = request.args.get('city', "")
    page = request.args.get('page', None)
    [start_pagination, end_pagination] = set_pagination(page)

    response = get_by_most_discount(city, start_pagination, end_pagination)
    return jsonify(response)  # render_template('', bussiness=response)


@bussiness_bp.route('/nearest', methods=['GET'])
def find_by_nearest():
    lat = request.args.get('lat', 0)
    lon = request.args.get('lon', 0)
    city = request.args.get('city', "")
    page = request.args.get('page', None)
    [start_pagination, end_pagination] = set_pagination(page)
    response = get_by_nearest(lat, lon, city, start_pagination, end_pagination)
    return jsonify(response)  # render_template('', bussiness=response)


@bussiness_bp.route('/top', methods=['GET'])
def find_top_rated():
    city = request.args.get('city')
    page = request.args.get('page', None)
    [start_pagination, end_pagination] = set_pagination(page)

    response = get_top_rated(city, start_pagination, end_pagination)
    return render_template('', bussiness=response)


@bussiness_bp.route('/newest', methods=['GET'])
def find_newest():
    city = request.args.get('city')
    page = request.args.get('page', None)
    [start_pagination, end_pagination] = set_pagination(page)

    response = get_newest(city, start_pagination, end_pagination)
    return render_template('', bussiness=response)


@bussiness_bp.route('/<slug>/<filter>', methods=['GET'])
def find_by_product_filter(slug, filter=filter_list['newest']):
    type = type_list['bussiness']
    if (filter not in filter_list):
        return ('error')
    city = request.args.get('city')
    page = request.args.get('page', None)
    [start_pagination, end_pagination] = set_pagination(page)
    if (filter == filter_list['top_rated']):
        response = top_rated_products(slug, start_pagination, end_pagination)
    elif (filter == filter_list['popular']):
        response = popular_products(slug, start_pagination, end_pagination)
    else:
        response = newest_products(slug, start_pagination, end_pagination)
    return render_template('', products=response)

# @bussiness_bp.route('/owner', methods=['GET'])
# def find_by_owner():
#     id = request.args.get('id')
#     response = get_by_owner(id)
#     print(response)
#     return 'Hello Bussiness!'


# @bussiness_bp.route('/owner/popular', methods=['GET'])
# def find_popular_by_owner():
#     id = request.args.get('id')
#     response = get_by_owner_popular(id)
#     print(response)
#     return 'Hello Bussiness!'
