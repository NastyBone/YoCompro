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
    if verify_existing_email(data.get("email")):
        return "Email already exists", 400
    if password != data.get("confirm-password"):
        return "Password does not match", 400
    if len(password) > 12 or len(password) < 8:
        return "Password must be 8-12 character long", 400
    regex_result = regex_password_match(password)
    if regex_result != True:
        print("here??")
        return regex_result, 400
    register_data = register(data)
    print(register_data)
    create_list(register_data.get("id"))
    return "Success!"


@auth_bp.route("/login", methods=["POST"])
def user_login():
    data = request.get_json()
    response = login(data["email"], data["password"])
    return jsonify(response)


@auth_bp.route("/logout", methods=["GET"])
@login_required()
def user_logout():
    logout()
    return jsonify(True)


@auth_bp.route("/register", methods=["GET"])
def register_form():
    return render_template("auth/register.html")


@auth_bp.route("/login", methods=["GET"])
def login_form():
    return render_template("auth/login.html")
