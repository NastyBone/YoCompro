from weakref import ref
from flask import Blueprint, jsonify, request, render_template, abort, session
from services.products_service import (
    get_by_search_tags as products_by_tag,
    get_popular as products_popular,
    get_newest as products_newest,
    get_top_rated as products_top,
)
from services.bussiness_service import (
    get_by_search_tags as bussiness_by_tag,
    get_by_nearest as bussiness_nearest,
    get_top_rated as bussiness_top,
    get_popular as bussiness_popular,
    get_by_most_discount as bussiness_discount,
)
from services.tags_service import get_all_by_status
from helpers import to_tag_ids, set_pagination, filter_list

search_bp = Blueprint("search", __name__)


@search_bp.route("/", methods=["GET"])
def general_search():
    [start_pagination, end_pagination] = set_pagination(None)
    city = session["city"]
    lat = session["lat"]
    lon = session["lon"]
    type = request.args.get("type", "products")
    filter = request.args.get("filter", "None")
    if filter == "None":
        if type == "products":
            [response, count] = products_by_tag(
                "", [], start_pagination, end_pagination
            )
        else:
            [response, count] = bussiness_by_tag(
                "", [], start_pagination, end_pagination
            )
    else:
        if filter not in filter_list:
            raise ValueError("Not in list")
        if type == "products":
            if "TOP_RATED" == filter_list[filter]:
                [response, count] = products_top(city, start_pagination, end_pagination)
            elif "NEWEST" == filter_list[filter]:
                [response, count] = products_newest(
                    city, start_pagination, end_pagination
                )
            else:
                [response, count] = products_popular(
                    city, start_pagination, end_pagination
                )
        else:
            if "TOP_RATED" == filter_list[filter]:
                [response, count] = bussiness_top(
                    city, start_pagination, end_pagination
                )
            elif "MOST_DISCOUNT" == filter_list[filter]:
                [response, count] = bussiness_discount(
                    city, start_pagination, end_pagination
                )
            elif "NEAREST" == filter_list[filter]:
                [response, count] = bussiness_nearest(
                    lat, lon, city, start_pagination, end_pagination
                )
            else:
                [response, count] = bussiness_popular(
                    city, start_pagination, end_pagination
                )
    available_tags = get_all_by_status("approved")
    return render_template(
        "search.html",
        items=response,
        pages=count / 12,  # 12 per page
        keyword="",
        tag_list=available_tags,
    )


@search_bp.route("/products", methods=["POST"])
def search_products():

    name = request.args.get("name", "")
    page = request.args.get("page", None)
    filter = request.args.get("filter", "")
    city = session["city"]
    [start_pagination, end_pagination] = set_pagination(page)
    data = request.get_json(silent=True)
    if data != None:
        tag_ids = list(map(int, data.get("tags", [])))
    else:
        tag_ids = []
    if name or filter == "None":
        [response, count] = products_by_tag(
            name, tag_ids, start_pagination, end_pagination
        )
    else:
        if filter not in filter_list:
            raise ValueError("Not in list")

        if "TOP_RATED" == filter_list[filter]:
            [response, count] = products_top(city, start_pagination, end_pagination)
        elif "NEWEST" == filter_list[filter]:
            [response, count] = products_newest(city, start_pagination, end_pagination)
        elif "POPULAR" == filter_list[filter]:
            [response, count] = products_popular(city, start_pagination, end_pagination)

    return jsonify({"data": response, "count": count / 12, "keyword": name})


@search_bp.route("/bussiness", methods=["POST"])
def search_bussiness():

    page = request.args.get("page")
    name = request.args.get("name", "")
    lat = session["lat"]
    lon = session["lon"]
    data = request.get_json(silent=True)
    city = session["city"]
    filter = request.args.get("filter", "")

    [start_pagination, end_pagination] = set_pagination(page)
    if data != None:
        tag_ids = list(map(int, data.get("tags", [])))
    else:
        tag_ids = []
    if name or filter == "None":
        [response, count] = bussiness_by_tag(
            name, tag_ids, start_pagination, end_pagination
        )
    else:
        if filter not in filter_list:
            raise ValueError("Not in list")

        if "TOP_RATED" == filter_list[filter]:
            [response, count] = bussiness_top(city, start_pagination, end_pagination)
        elif "MOST_DISCOUNT" == filter_list[filter]:
            [response, count] = bussiness_discount(
                city, start_pagination, end_pagination
            )
        elif "NEAREST" == filter_list[filter]:
            [response, count] = bussiness_nearest(
                lat, lon, city, start_pagination, end_pagination
            )
        else:
            [response, count] = bussiness_popular(
                city, start_pagination, end_pagination
            )

    return jsonify({"data": response, "count": count / 12, "keyword": name})
    # return render_template("search.html", items=response, keyword=name)
