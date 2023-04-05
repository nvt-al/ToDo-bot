from flask import Flask, render_template, url_for, redirect, flash, request
from flask_migrate import Migrate
from flask_login import LoginManager

from webapp.models import db
from webapp.views import page
from webapp.user.models import User
from webapp.user.views import blueprint as user_blueprint



def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config.from_pyfile("config.py")
    db.init_app(app)
    migrate = Migrate(app, db)
    app.register_blueprint(page)
    app.register_blueprint(user_blueprint)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    return app
