from flask import Blueprint, request, render_template, redirect, session
from guard import *
from services.auth_service import *
from services.products_service import (
    get_newest_limited,
    get_popular_limited as product_popular,
    get_top_rated_limited as product_top_rated,
)
from services.bussiness_service import (
    get_popular_limited as bussiness_popular,
    get_by_nearest_limited,
    get_by_most_discount_limited,
    get_top_rated_limited as bussiness_top_rated,
)

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/", methods=["GET"])
def main():
    city = session["city"]
    lat = session["lat"]
    lon = session["lon"]
    if not city:
        return redirect("/allow-location")
    popular_products = product_popular(city)
    newest_products = get_newest_limited(city)
    nearest_bussiness = get_by_nearest_limited(lat, lon, city)
    popular_bussiness = bussiness_popular(city)
    most_discount = get_by_most_discount_limited(city)
    top_products = product_top_rated(city)
    top_bussiness = bussiness_top_rated(city)
    print("new", newest_products)
    return render_template(
        "dashboards/client_dashboard.html",
        popular_products=popular_products,
        newest_products=newest_products,
        nearest_bussiness=nearest_bussiness,
        popular_bussiness=popular_bussiness,
        most_discount=most_discount,
        top_bussiness=top_bussiness,
        top_products=top_products,
    )
