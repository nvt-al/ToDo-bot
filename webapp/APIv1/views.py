from flask import Blueprint, jsonify
from flask_login import current_user

from webapp.models import TaskTemplates

blueprint = Blueprint("APIv1", __name__, url_prefix="/todo/api/v1.0/tasks")


@blueprint.route("/", methods=["GET"])
def get_tasks():
    pass
    # return jsonify({'tasks': tasks})


@blueprint.route("/templates", methods=["GET"])
def get_task_templates():
    task_templates = TaskTemplates.query.filter_by(owner=current_user.id).all()
    return jsonify({"task_templates": task_templates})


# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for("index"))
#     title = "Авторизация"
#     login_form = LoginForm()
#     return render_template("user/login.html", page_title=title, form=login_form)
