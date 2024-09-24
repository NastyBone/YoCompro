from flask import Flask
from flask_login import LoginManager
from flask_session import Session
from services.users_service import get_with_password
from classes.users_class import UserLogin
from routes.__index__ import *
import secrets
# INIT CONFIG
app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_urlsafe(24)
# BLUEPRINTS
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(brands_bp, url_prefix='/brands')
app.register_blueprint(bussiness_bp, url_prefix='/bussiness')
app.register_blueprint(lists_bp, url_prefix='/lists')
app.register_blueprint(products_bp, url_prefix='/products')
app.register_blueprint(ratings_bp, url_prefix='/ratings')
app.register_blueprint(stocks_bp, url_prefix='/stocks')
app.register_blueprint(owner_bp, url_prefix='/owner')
app.register_blueprint(tags_bp, url_prefix='/tags')
app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(search_bp, url_prefix='/search')
app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
# SESSION
app.config['SESSION_TYPE'] = 'filesystem'
login_manager = LoginManager()
login_manager.init_app(app)
app.config.from_object(__name__)
Session(app)


@login_manager.user_loader
def load_user(userid):
    user = get_with_password(userid)[0]
    user_login = UserLogin(
        id=user['id'], name=user['name'], email=user['email'], role=user['role'], password=user['password'])
    return user_login


@app.route('/')
def index():
    return 'Hello App!'


if __name__ == '__app__':
    app.run(debug=True)

# TODO: Change jsonify from routes to actual render an html
