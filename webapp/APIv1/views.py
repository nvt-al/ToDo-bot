from flask import Blueprint, jsonify
from flask_login import current_user

from webapp.models import Tasks, TaskTemplates

blueprint = Blueprint("APIv1", __name__, url_prefix="/todo/api/v1.0/tasks")


@blueprint.route("/", methods=["GET"])
def get_tasks():
    query = Tasks.query.filter(Tasks.id_list == current_user.active_list).all()
    tasks = []
    for task in query:
        tasks.append(
            {
                "task_id": task.id,
                "name": task.task_template.name,
                "description": task.task_template.description,
                "task_done": task.task_done,
            }
        )
    return jsonify({"tasks": tasks})


# Возвращает все записи, а должен только этого пользователя


@blueprint.route("/templates", methods=["GET"])
def get_task_templates():
    task_templates = TaskTemplates.query.filter_by(owner=current_user.id).all()
    print([i.serialize for i in task_templates])
    return jsonify({"task_templates": [i.serialize for i in task_templates]})
