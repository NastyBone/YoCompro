from flask import Blueprint, request, jsonify, Response
from guard import *
from helpers import roles_list
from services.auth_service import *
auth_bp = Blueprint("auth", __name__)


@auth_bp.route('/')
@role_required(roles_list['admin'])
def index():
    return 'Hello Auth!'


@auth_bp.route('/register', methods=['POST'])
@logged_in_guard()
def user_register():
    data = request.get_json()
    return register(data)


@auth_bp.route('/login', methods=['POST'])
@logged_in_guard()
def user_login():
    data = request.get_json()
    response = login(data['email'], data['password'])
    return jsonify(response)


@auth_bp.route('/logout', methods=['GET'])
@login_required()
def user_logout():
    logout()
    return jsonify(True)
