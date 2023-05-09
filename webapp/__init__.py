import logging

from flask import Flask, render_template
from flask_login import LoginManager
from flask_migrate import Migrate

from webapp.APIv1.views import blueprint as APIv1_blueprint
from webapp.db import db
from webapp.task_templates.views import blueprint as task_template_blueprint
from webapp.todo.views import blueprint as task_blueprint
from webapp.user.models import User
from webapp.user.views import blueprint as user_blueprint

logging.basicConfig(
    filename="webapp.log",
    level=logging.INFO,
    format="%(lineno)d #%(levelname)-8s " "[%(asctime)s] - %(name)s - %(message)s",
)


def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config.from_pyfile("config.py")
    db.init_app(app)
    migrate = Migrate(app, db)

    app.register_blueprint(task_template_blueprint)
    app.register_blueprint(task_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(APIv1_blueprint)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login"

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    return app
