
from functools import wraps
from flask_login import current_user
from flask import abort, request, redirect


def role_required(role_name):
    def decorator(func):
        @wraps(func)
        def authorize(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(401)  # Unauthorized access
                redirect('/unauthorized')

            if not current_user.has_role(role_name):
                abort(403)  # Forbidden access (wrong role)
                redirect('/forbidden')

            return func(*args, **kwargs)
        return authorize
    return decorator


def login_required():
    def decorator(func):
        @wraps(func)
        def check_log(*args, **kwargs):
            if not current_user:
                print('redirect to log in')
                redirect('/auth/login')
            return func(*args, **kwargs)
        return check_log
    return decorator


def logged_in_guard():
    def decorator(func):
        @wraps(func)
        def check_no_log(*args, **kwargs):
            if current_user.is_authenticated:
                print('redirect to dashboard')
                redirect('/auth/dashboard')
            return func(*args, **kwargs)
        return check_no_log
    return decorator


def secure_access():
    def decorator(func):
        @wraps(func)
        def check_if_belongs(*args, **kwargs):
            logged_id = current_user.get_id()
            id = request.args.get('user_id', request.args.get('owner_id', 0))
            if (int(id) != logged_id):
                abort(401)
                redirect('/unauthorized')
            return func(*args, **kwargs)
        return check_if_belongs
    return decorator
