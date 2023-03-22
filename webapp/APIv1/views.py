from flask import Blueprint, jsonify
from flask_login import current_user
from sqlalchemy import text

from webapp.models import Tasks, TaskTemplates, db

blueprint = Blueprint("APIv1", __name__, url_prefix="/todo/api/v1.0/tasks")


@blueprint.route("/", methods=["GET"])
def get_tasks():
    query = (
        db.session.query(Tasks, TaskTemplates)
        .join(TaskTemplates, Tasks.id_task == TaskTemplates.id)
        .filter(Tasks.id_list == current_user.active_list)
        .filter(TaskTemplates.owner == current_user.id)
        .all()
    )

    # query = """
    #         SELECT tasks.id, id_list, task_done, name, description
    #         FROM tasks LEFT JOIN task_templates on tasks.id_task == task_templates.id
    #         WHERE id_list == 10 AND owner == 1
    #         """

    # tasks = db.session.execute(text(query), current_user.active_list).all()
    # print(tasks)

    tasks = []
    for task in query:
        tasks.append(
            {
                "task_id": task[0].id,
                "name": task[1].name,
                "description": task[1].description,
                "task_done": task[0].task_done,
            }
        )
    return jsonify({"tasks": tasks})


@blueprint.route("/templates", methods=["GET"])
def get_task_templates():
    task_templates = TaskTemplates.query.filter_by(owner=current_user.id).all()
    print([i.serialize for i in task_templates])
    return jsonify({"task_templates": [i.serialize for i in task_templates]})
