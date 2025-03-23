from flask import Blueprint, request, jsonify, session, render_template
from guard import login_required
from services.stats_service import (
    bussiness_stats as bussiness,
    products_stats as products,
    tags_stats as tags,
    users_stats as users,
)
from helpers import set_pagination, status_list, type_list, roles_list
from services.products_service import get_by_status as products_by_status
from services.bussiness_service import get_by_status as bussinnes_by_status
from services.tags_service import get_by_status as tags_by_status
from services.users_service import get as get_user, update_role, update as update_user

# TODO: Protect
admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/", methods=["GET"])
def stats():
    bussiness_stats = bussiness()
    users_stats = users()
    products_stats = products()
    tags_stats = tags()
    return render_template(
        "dashboards/admin_dashboard.html",
        bussiness=bussiness_stats,
        users=users_stats,
        products=products_stats,
        tags=tags_stats,
    )


@admin_bp.route("/search", methods=["GET"])
def general_search():

    type = request.args.get("type", "products")
    [start_pagination, end_pagination] = set_pagination(None)
    if type == "products":
        [response, count] = products_by_status(
            "approved", start_pagination, end_pagination, ""
        )
    elif type == "bussiness":
        [response, count] = bussinnes_by_status(
            "approved", start_pagination, end_pagination, ""
        )
    elif type == "tags":
        [response, count] = tags_by_status(
            "approved", start_pagination, end_pagination, ""
        )
    else:
        [response, count] = products_by_status(  # users by status
            "approved", start_pagination, end_pagination, ""
        )

    return render_template(
        "search/admin_search.html",
        items=response,
        pages=count / 12,  # 12 per page
    )


@admin_bp.route("/profile-edit", methods=["GET"])
@login_required()
def edit_profile_from_admin():
    id = request.args.get("id")
    response = get_user(id)
    return render_template("admin/edit_user.html", user=response)


@admin_bp.route("/edit-user", methods=["PUT"])
@login_required()
def update_profile_from_admin():
    data = request.get_json()
    id = request.args.get("id")
    if data.get("role") not in roles_list:
        return "Role not found", 400
    update_user(id, data)
    update_role(id, data.get("role"))
    return "Success!"
