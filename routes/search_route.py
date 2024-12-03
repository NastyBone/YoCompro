from weakref import ref
from flask import Blueprint, jsonify, request, render_template, abort
from services.products_service import get_by_search_tags as search_product
from services.bussiness_service import get_by_search_tags as bussiness_by_tag
from services.tags_service import get_by_status
from helpers import to_tag_ids, set_pagination, roles_list

search_bp = Blueprint("search", __name__)


@search_bp.route("/", methods=["GET"])
def general_search():
    [start_pagination, end_pagination] = set_pagination(None)
    available_tags = get_by_status("approved")
    [response, count] = search_product("", [], start_pagination, end_pagination)
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

    [start_pagination, end_pagination] = set_pagination(page)
    data = request.get_json(silent=True)
    if data != None:
        tag_ids = list(map(int, data.get("tags", [])))
    else:
        tag_ids = []
    [response, count] = search_product(name, tag_ids, start_pagination, end_pagination)

    return jsonify({"data": response, "count": count / 12, "keyword": name})


@search_bp.route("/bussiness", methods=["POST"])
def search_bussiness():

    page = request.args.get("page")
    name = request.args.get("name", "")
    data = request.get_json(silent=True)
    [start_pagination, end_pagination] = set_pagination(page)
    if data != None:
        tag_ids = list(map(int, data.get("tags", [])))
    else:
        tag_ids = []
    [response, count] = bussiness_by_tag(
        name, tag_ids, start_pagination, end_pagination
    )
    return jsonify({"data": response, "count": count / 12, "keyword": name})
    # return render_template("search.html", items=response, keyword=name)
