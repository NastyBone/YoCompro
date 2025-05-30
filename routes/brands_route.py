from flask import Blueprint, redirect, request, jsonify, render_template, session
from guard import role_required
from services.brands_service import *
from helpers import (
    filter_list,
    roles_list,
    slug_generator,
    type_list,
    set_pagination,
    generate_filename,
)
from services.products_service import (
    get_popular_by_brand as products_popular,
    get_newest_by_brand as produscts_newest,
    get_top_rated_by_brand as products_top_rated,
)
from services.bussiness_service import get_popular_by_brand as bussiness_popular
import bcrypt
from services.images_service import insert as insert_image, update as update_image

brands_bp = Blueprint("brands", __name__)

# BASIC DONE


@brands_bp.route("/test")
def index():
    return "Hello Brands!"


@brands_bp.route("/", methods=["GET"])
def find():
    id = request.args.get("id")
    response = get(id)
    return jsonify(response)


@brands_bp.route("/all", methods=["GET"])
def find_all():
    response = get_all()
    return jsonify(response)


@brands_bp.route("/", methods=["POST"])
@role_required("ADMIN")
def create():
    data = request.form
    image = request.files.get("image")
    image_name = generate_filename(image.filename)
    path = f"static/images/brands/{image_name}"
    response = insert(
        {
            "name": data.get("name"),
            "country": data.get("country"),
            "slug": slug_generator(data.get("name")),
        }
    )
    image.save(path)
    insert_image(image_name, response[0]["id"], "/" + path, "images_brands", "brand_id")
    return jsonify(response)


@brands_bp.route("/", methods=["PUT"])
@role_required("ADMIN")
def edit():
    data = request.form
    id = request.args.get("id")
    response = update(
        id,
        {
            "name": data.get("name"),
            "country": data.get("country"),
            "slug": slug_generator(data.get("name")),
        },
    )
    image = request.files.get("image")
    if image:
        image_name = generate_filename(image.filename)
        path = f"static/images/brands/{image_name}"
        image.save(path)
        update_image(
            image_name,
            response[0]["id"],
            "/" + path,
            "images_brands",
            "brand_id",
        )
    return jsonify(response)


@brands_bp.route("/", methods=["DELETE"])
def remove():
    id = request.args.get("id")
    response = delete(id)
    return "Success!"


@brands_bp.route("/", methods=["PATCH"])
def edit_status():
    status = request.get_json()["status"]
    id = request.args.get("id")
    response = update_status(id, status)
    return "Success!"


@brands_bp.route("/form", methods=["GET"])
def form():
    id = request.args.get("id", None)
    if id:
        brand = get(id)
    else:
        brand = [None]
    return render_template("form_create/form_create_brand.html", brand=brand)


@brands_bp.route("/edit/form", methods=["GET"])
def edit_form():
    return render_template("")


#################################################


@brands_bp.route("/<slug>/bussiness/")
def popular_bussines(slug):
    city = session.get("city")
    page = request.args.get("page", None)
    [start_pagination, end_pagination] = set_pagination(page)
    response = bussiness_popular(city, slug, start_pagination, end_pagination)
    return response


@brands_bp.route("/<slug>/search/products", methods=["GET"])
def find_by_product_filter(slug):
    page = request.args.get("page", None)
    filter = request.args.get("filter", "popular")
    json = request.args.get("json", False)
    name = request.args.get("name", "")
    if filter not in filter_list:
        return "error"
    brand = get_with_details(slug)
    [start_pagination, end_pagination] = set_pagination(page)
    if filter == "top_rated":
        [response, count] = products_top_rated(
            slug, False, start_pagination, end_pagination, word=name
        )
    elif filter == "popular":
        [response, count] = products_popular(
            slug, False, start_pagination, end_pagination, word=name
        )
    else:
        [response, count] = produscts_newest(
            slug, False, start_pagination, end_pagination, word=name
        )
    if json:
        return jsonify({"data": response, "count": count / 12})
    return render_template(
        "search/brand_search.html",
        items=response,
        brand=brand,
        count=count,
        pages=count / 12,
    )


@brands_bp.route("/search/<slug>", methods=["GET"])
def find_by_slug(slug):
    city = session.get("city")
    response = get_with_details(slug)
    [popular, count] = products_popular(slug, True)
    [top_rated, count] = products_top_rated(slug, True)
    [newest, count] = produscts_newest(slug, True)
    [bussiness, count] = bussiness_popular(city, slug, True)
    print("aaaa", response)
    return render_template(
        "details/detail_brand.html",
        brand=response,
        popular=popular,
        top_rated=top_rated,
        newest=newest,
        bussiness=bussiness,
    )


@brands_bp.route("/<status>", methods=["GET"])
def get_brands_by_status(status):
    if status not in status_list:
        return "error"
    name = request.args.get("name", "")
    page = request.args.get("page", None)
    [start_pagination, end_pagination] = set_pagination(page)
    [response, count] = get_by_status(status, start_pagination, end_pagination, name)
    print(response)
    return jsonify({"data": response, "count": count / 12})
