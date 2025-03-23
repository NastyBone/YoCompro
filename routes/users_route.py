from helpers import roles_list
from guard import role_required
from flask import Blueprint, request, jsonify, render_template
from flask_login import current_user
from services.auth_service import verify_existing_email
from services.lists_services import get_by_user as list_user
from services.ratings_service import get_by_user as ratings_user
from services.users_service import *
from guard import login_required, secure_access

users_bp = Blueprint("users", __name__)


# BASIC #DONE


@users_bp.route("/test", methods=["GET"])
def index():
    return "Hello Users!"


@users_bp.route("/", methods=["GET"])
@role_required(roles_list["admin"])
def find():
    id = request.args.get("id")
    response = get(id)
    return jsonify(response)


@users_bp.route("/all", methods=["GET"])
def find_all():
    response = get_all()
    return jsonify(response)


@users_bp.route("/", methods=["POST"])
def create():
    data = request.get_json()
    response = insert(data)
    return jsonify(response)


@users_bp.route("/", methods=["PUT"])
def edit():
    id = current_user.get_id() or 3
    data = request.get_json()
    if verify_existing_email(data.get("email")):
        return "Email already exists", 400
    response = update(id, data)
    return "Success!"


@users_bp.route("/", methods=["DELETE"])
def remove():
    id = request.args.get("id")
    response = delete(id)
    return jsonify(True)


# CLIENT


# @users_bp.route("/become-owner", methods=["GET"])
# @login_required()
# def become_owner():
# TODO: check if user is already an owner
# TODO: logic for create bussiness
# return render_template("create_owner")


@users_bp.route("/profile-edit", methods=["GET"])
@login_required()
def edit_profile():
    id = current_user.get_id() or 3
    print("ID", id)
    response = get(id)
    return render_template("auth/form_edit_user.html", user=response)


@users_bp.route("/admin/update-role", methods=["GET"])
@login_required()
def edit_role():
    id = current_user.get_id() or 3
    response = get(id)
    return render_template("auth/form_edit_user.html", user=response)


@users_bp.route("/my-list", methods=["GET"])
@secure_access()
def get_list():
    response = list_user(request.args.get("user_id"))
    return jsonify(response)


@users_bp.route("/my-ratings", methods=["GET"])
def get_ratings():
    response = ratings_user(current_user.get_id())
    return render_template("", ratings=response)
