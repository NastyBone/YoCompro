from flask import Blueprint, request, render_template, redirect
from guard import *
from services.auth_service import *
from services.products_service import get_newest_limited, get_popular_limited as product_popular, get_top_rated_limited as product_top_rated
from services.bussiness_service import get_popular_limited as bussiness_popular, get_by_nearest_limited, get_by_most_discount_limited
dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route('/', methods=['GET'])
def main():
    city = request.form.get('city')
    lat = request.form.get('lat')
    lon = request.form.get('lon')
    if (not city):
        print('Render Allow Location View')
    popular_products = product_popular(city)
    newest_products = get_newest_limited(city)
    nearest_bussiness = get_by_nearest_limited(lat, lon, city)
    popular_bussiness = bussiness_popular(city)
    most_discount = get_by_most_discount_limited(city)
    top_products = product_top_rated(city)

    return render_template('',
                           popular_products=popular_products, newest_products=newest_products, nearest_bussiness=nearest_bussiness, popular_bussiness=popular_bussiness, most_discount=most_discount,
                           top_products=top_products)


@dashboard_bp.route('/allow-location', methods=['GET'])
def allow_location():
    return render_template('')


@dashboard_bp.route('/not-found', methods=['GET'])
def not_found():
    return render_template('')


@dashboard_bp.route('/forbidden', methods=['GET'])
def forbidden():
    return render_template('')


@dashboard_bp.route('/error', methods=['GET'])
def exception():
    return render_template('')
