from flask import Flask, render_template
from flask_migrate import Migrate

from webapp.models import db
from webapp.user.forms import LoginForm


def create_app():
    app = Flask(__name__)

    app.config.from_pyfile("config.py")
    db.init_app(app)
    migrate = Migrate(app, db)

    @app.route("/login")
    def login():
        title = "Авторизация"
        login_form = LoginForm()
        return render_template("user/login.html", page_title=title, form=login_form)

    return app
