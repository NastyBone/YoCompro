from flask import Flask, redirect, render_template, request, url_for, session as sess
from flask_login import LoginManager
from flask_session import Session
import werkzeug
from services.users_service import get_with_password
from classes.users_class import UserLogin
from routes.__index__ import *
from location import set_location, asked_location
import secrets

# INIT CONFIG
app = Flask(__name__)
app.config["SECRET_KEY"] = secrets.token_urlsafe(24)
# BLUEPRINTS
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(brands_bp, url_prefix="/brands")
app.register_blueprint(bussiness_bp, url_prefix="/bussiness")
app.register_blueprint(lists_bp, url_prefix="/lists")
app.register_blueprint(products_bp, url_prefix="/products")
app.register_blueprint(ratings_bp, url_prefix="/ratings")
app.register_blueprint(stocks_bp, url_prefix="/stocks")
app.register_blueprint(owner_bp, url_prefix="/owner")
app.register_blueprint(tags_bp, url_prefix="/tags")
app.register_blueprint(users_bp, url_prefix="/users")
app.register_blueprint(search_bp, url_prefix="/search")
app.register_blueprint(dashboard_bp, url_prefix="/dashboard")
# SESSION
app.config["SESSION_TYPE"] = "filesystem"
login_manager = LoginManager()
login_manager.init_app(app)
app.config.from_object(__name__)
session = Session(app)


@login_manager.user_loader
def load_user(userid):
    user = get_with_password(userid)[0]
    user_login = UserLogin(
        id=user["id"],
        name=user["name"],
        email=user["email"],
        role=user["role"],
        password=user["password"],
    )
    return user_login


@app.route("/")
def index():
    return render_template("misc/allow_location.html")


@app.route("/allow-location", methods=["GET"])
def allow_location():
    asked_location(True)
    print("askin")
    return render_template("misc/allow_location.html")


@app.route("/refresh-location", methods=["GET"])
def refresh_location():
    print("reseting")
    asked_location(None)
    return "", 201


@app.route("/not-found", methods=["GET"])
def not_found():
    return render_template("misc/not_found.html")


@app.errorhandler(werkzeug.exceptions.NotFound)
def handle_bad_request(e):
    return redirect("/not-found")


@app.route("/unauthorized", methods=["GET"])
def unauthorized():
    return render_template("misc/not_authorized.html")


@app.route("/forbidden", methods=["GET"])
def forbidden():
    return render_template("misc/forbidden.html")


@app.errorhandler(werkzeug.exceptions.Forbidden)
def handle_bad_request(e):
    return redirect("/forbidden")


@app.route("/error", methods=["GET"])
def exception():
    return render_template("misc/error.html")


@app.errorhandler(werkzeug.exceptions.InternalServerError)
def handle_bad_request(e):
    return redirect("/error")


@app.route("/handle_location", methods=["POST"])
def check_location():
    data = request.get_json()
    if data:
        location = set_location(data["latitude"], data["longitude"])
        if not location:
            return "", 500
        else:
            return "", 201
    return "", 500


if __name__ == "__app__":
    app.run(debug=True)
