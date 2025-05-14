from flask import Blueprint, request, render_template, redirect, jsonify
from guard import *
from flask_login import current_user
from helpers import roles_list, set_pagination, filter_list
from services.products_service import (
    get_popular_by_owner as products_popular,
    get_top_rated_by_owner as products_top_rated,
)
from services.brands_service import *
from services.bussiness_service import (
    get_by_owner_popular as bussiness_popular,
    get_by_owner as bussiness_all,
    get_by_owner_top_rated as bussiness_top_rated,
)
from services.stocks_service import get_by_bussiness as stock_bussiness

owner_bp = Blueprint("owner", __name__)


@owner_bp.route("/dashboard", methods=["GET"])
def main():
    owner = current_user.get_id() or 3
    [popular_products, count] = products_popular(owner, limited=True)
    [popular_bussiness, count] = bussiness_popular(owner, limited=True)
    [unpopular_bussiness, count] = bussiness_popular(owner, limited=True, order="ASC")
    [unpopular_products, count] = products_popular(owner, limited=True, order="ASC")
    [top_rated_bussiness, count] = bussiness_top_rated(owner, limited=True)
    [top_rated_products, count] = products_top_rated(owner, limited=True)
    [less_rated_bussiness, count] = bussiness_top_rated(
        owner, limited=True, order="ASC"
    )
    [less_rated_products, count] = products_top_rated(owner, limited=True, order="ASC")
    # print("wut")
    # print(popular_products)
    return render_template(
        "/dashboards/owner_dashboard.html",
        popular_products=popular_products,
        popular_bussiness=popular_bussiness,
        less_rated_products=less_rated_products,
        top_rated_products=top_rated_products,
        unpopular_bussiness=unpopular_bussiness,
        unpopular_products=unpopular_products,
        top_rated_bussiness=top_rated_bussiness,
        less_rated_bussiness=less_rated_bussiness,
    )
    # return render_template('',
    #                        popular_products=popular_products, popular_bussiness=popular_bussiness,
    #                        unpopular_bussiness=unpopular_bussiness)


@owner_bp.route("/search", methods=["GET"])
def general_search():
    owner_id = current_user.get_id()
    type = request.args.get("type", "products")
    filter = request.args.get("filter", "popular")
    [start_pagination, end_pagination] = set_pagination(None)
    if type == "products":
        if filter == "popular":
            print("OWNER ID", owner_id)
            [response, count] = products_popular(
                owner_id, False, start_pagination, end_pagination
            )
        elif filter == "top_rated":
            [response, count] = products_top_rated(
                owner_id, False, start_pagination, end_pagination
            )
        elif filter == "less_rated":
            [response, count] = products_top_rated(
                owner_id, False, start_pagination, end_pagination, order="ASC"
            )
        elif filter == "unpopular":
            [response, count] = products_popular(
                owner_id, False, start_pagination, end_pagination, order="ASC"
            )
    elif type == "bussiness":
        if filter == "popular":
            [response, count] = bussiness_popular(
                owner_id, False, start_pagination, end_pagination
            )
        elif filter == "top_rated":
            [response, count] = bussiness_top_rated(
                owner_id, False, start_pagination, end_pagination
            )
        elif filter == "less_rated":
            [response, count] = bussiness_top_rated(
                owner_id, False, start_pagination, end_pagination, order="ASC"
            )
        elif filter == "unpopular":
            [response, count] = bussiness_popular(
                owner_id, False, start_pagination, end_pagination, order="ASC"
            )

    return render_template(
        "search/owner_search.html",
        items=response,
        pages=count / 12,  # 12 per page
    )


@owner_bp.route("/bussiness/popular", methods=["GET"])
def popular_bussiness():
    page = request.args.get("page", None)
    name = request.args.get("name", "")
    status = request.args.get("status", None)
    if status not in status_list:
        return "error"
    owner = current_user.get_id()
    [start_pagination, end_pagination] = set_pagination(page)
    [response, count] = bussiness_popular(
        owner,
        start_page=start_pagination,
        end_page=end_pagination,
        order="ASC",
        word=name,
        status=status,
    )
    return jsonify({"data": response, "count": count / 12})
    # return render_template('', bussiness=response)


@owner_bp.route("/bussiness/unpopular", methods=["GET"])
def unpopular_bussiness():
    page = request.args.get("page", None)
    name = request.args.get("name", "")
    status = request.args.get("status", None)
    if status not in status_list:
        return "error"
    owner = current_user.get_id()
    [start_pagination, end_pagination] = set_pagination(page)
    [response, count] = bussiness_popular(
        owner,
        start_page=start_pagination,
        end_page=end_pagination,
        word=name,
        status=status,
    )
    return jsonify({"data": response, "count": count / 12})

    # return render_template('', bussiness=response)


@owner_bp.route("/products/popular", methods=["GET"])
def popular_products():
    page = request.args.get("page", None)
    name = request.args.get("name", "")
    status = request.args.get("status", None)
    if status not in status_list:
        return "error"
    owner = current_user.get_id()
    [start_pagination, end_pagination] = set_pagination(page)
    [response, count] = products_popular(
        owner,
        start_page=start_pagination,
        end_page=end_pagination,
        word=name,
        status=status,
    )
    return jsonify({"data": response, "count": count / 12})

    # return render_template('', products=response)


@owner_bp.route("/bussiness/less_rated", methods=["GET"])
def less_rated_bussiness():
    page = request.args.get("page", None)
    name = request.args.get("name", "")
    status = request.args.get("status", None)
    if status not in status_list:
        return "error"
    owner = current_user.get_id()
    [start_pagination, end_pagination] = set_pagination(page)
    [response, count] = bussiness_top_rated(
        owner,
        start_page=start_pagination,
        end_page=end_pagination,
        order="ASC",
        word=name,
        status=status,
    )
    return jsonify({"data": response, "count": count / 12})

    # return render_template('', products=response)


@owner_bp.route("/bussiness/top_rated", methods=["GET"])
def top_rated_bussiness():
    page = request.args.get("page", None)
    name = request.args.get("name", "")
    status = request.args.get("status", None)
    if status not in status_list:
        return "error"
    owner = current_user.get_id()
    [start_pagination, end_pagination] = set_pagination(page)
    [response, count] = bussiness_top_rated(
        owner,
        start_page=start_pagination,
        end_page=end_pagination,
        word=name,
        status=status,
    )
    return jsonify({"data": response, "count": count / 12})

    # return render_template('', products=response)


@owner_bp.route("/products/top_rated", methods=["GET"])
def top_rated_products():
    page = request.args.get("page", None)
    name = request.args.get("name", "")
    status = request.args.get("status", None)
    if status not in status_list:
        return "error"
    owner = current_user.get_id()
    [start_pagination, end_pagination] = set_pagination(page)
    [response, count] = products_top_rated(
        owner,
        start_page=start_pagination,
        end_page=end_pagination,
        word=name,
        status=status,
    )
    return jsonify({"data": response, "count": count / 12})

    # return render_template('', products=response)


@owner_bp.route("/products/less_rated", methods=["GET"])
def less_rated_products():
    page = request.args.get("page", None)
    name = request.args.get("name", "")
    status = request.args.get("status", None)
    if status not in status_list:
        return "error"
    owner = current_user.get_id()
    [start_pagination, end_pagination] = set_pagination(page)
    [response, count] = products_top_rated(
        owner,
        start_page=start_pagination,
        end_page=end_pagination,
        order="ASC",
        word=name,
        status=status,
    )
    return jsonify({"data": response, "count": count / 12})

    # return render_template('', products=response)


@owner_bp.route("/products/unpopular", methods=["GET"])
def unpopular_products():
    page = request.args.get("page", None)
    name = request.args.get("name", "")
    status = request.args.get("status", None)
    if status not in status_list:
        return "error"
    owner = current_user.get_id()
    [start_pagination, end_pagination] = set_pagination(page)
    [response, count] = products_popular(
        owner,
        start_page=start_pagination,
        end_page=end_pagination,
        order="ASC",
        word=name,
        status=status,
    )
    return jsonify({"data": response, "count": count / 12})

    # return render_template('', products=response)


@owner_bp.route("/<slug>/stocks", methods=["GET"])
def stocks(slug):
    owner = current_user.get_id()
    page = request.args.get("page", None)
    name = request.args.get("name", "")
    status = request.args.get("status", None)
    if status not in status_list:
        return "error"
    [start_pagination, end_pagination] = set_pagination(page)
    [response, count] = stock_bussiness(slug, owner, start_pagination, end_pagination)
    return jsonify({"data": response, "count": count / 12})

    # return render_template('', stocks=response)
