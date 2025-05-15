from functools import wraps
from flask_login import current_user
from flask import abort, request, redirect
from services.stocks_service import get as get_stock
from services.bussiness_service import get as get_bussiness


def role_required(role_name):
    def decorator(func):
        @wraps(func)
        def authorize(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(401)  # Unauthorized access
                redirect("/unauthorized")

            if not current_user.has_role(role_name):
                abort(403)  # Forbidden access (wrong role)
                redirect("/forbidden")

            return func(*args, **kwargs)

        return authorize

    return decorator


def login_required():
    def decorator(func):
        @wraps(func)
        def check_log(*args, **kwargs):
            if not current_user:
                redirect("/auth/login")
            return func(*args, **kwargs)

        return check_log

    return decorator


def logged_in_guard():
    def decorator(func):
        @wraps(func)
        def check_no_log(*args, **kwargs):
            if current_user.is_authenticated:
                redirect("/auth/dashboard")
            return func(*args, **kwargs)

        return check_no_log

    return decorator


def secure_access():
    def decorator(func):
        @wraps(func)
        def check_if_belongs(*args, **kwargs):
            logged_id = current_user.get_id()
            id = request.args.get("user_id", request.args.get("owner_id", 0))
            if int(id) != logged_id:
                abort(401)
                return redirect("/unauthorized")
            return func(*args, **kwargs)

        return check_if_belongs

    return decorator


def belongs_to_owner():
    def decorator(func):
        @wraps(func)
        def authorize(*args, **kwargs):
            if request.method == "PUT":
                logged_id = current_user.get_id()
                if request.json:
                    id = request.json.get("bussiness_id", 0)
                else:
                    id = 0
                id = int(id)
                if id != 0:
                    id = get_stock(int(request.args.get("id")))[0].get("bussiness_id")
                else:
                    id = request.form.get("id")
                bussiness = get_bussiness(id)
                if bussiness[0].get("user_id") != logged_id:
                    return "ERROR", 401
            return func(*args, **kwargs)

        return authorize

    return decorator
