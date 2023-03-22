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
    print([i.serialize for i in task_templates])
    return jsonify([i.serialize for i in task_templates])
