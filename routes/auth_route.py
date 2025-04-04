from flask import Blueprint, render_template, request, jsonify, Response
from guard import *
from helpers import roles_list, regex_password_match
from services.auth_service import *
from services.lists_services import insert as create_list

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/")
@role_required(roles_list["admin"])
def index():
    return "Hello Auth!"


@auth_bp.route("/register", methods=["POST"])
def user_register():
    data = request.get_json()
    password = data.get("password")
    if password != data.get("confirm-password"):
        return "Password does not match", 400
    if verify_existing_email(data.get("email")):
        return "Email already exists", 400
    verify_password(password)
    register_data = register(data)
    create_list(register_data.get("id"))
    return "Success!"


@auth_bp.route("/login", methods=["POST"])
def user_login():
    data = request.get_json()
    verify_password(data.get("password"))
    response = login(data["email"], data["password"])
    if isinstance(response, ValueError):
        return response.args[0], 400
    return "Success!", 200


@auth_bp.route("/password", methods=["PUT"])
def edit_password():
    id = current_user.get_id() or 3
    data = request.get_json()
    password = data.get("password")
    if password != data.get("confirm-password"):
        return "Password does not match", 400
    update_password(id, password)
    return "Success!"


@auth_bp.route("/logout", methods=["GET"])
@login_required()
def user_logout():
    logout()
    return "Success!", 200


@auth_bp.route("/register", methods=["GET"])
def register_form():
    return render_template("auth/register.html")


@auth_bp.route("/login", methods=["GET"])
def login_form():
    return render_template("auth/login.html")


def verify_password(password):
    if len(password) > 12 or len(password) < 8:
        return "Password must be 8-12 character long", 400
    regex_result = regex_password_match(password)
    if regex_result != True:
        return regex_result, 400
