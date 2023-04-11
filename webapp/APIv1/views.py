from dataclasses import dataclass

from flask import Blueprint, abort, jsonify, make_response, request, url_for
from sqlalchemy import func

# from webapp.APIv1.decorators import login_required_API
from webapp.models import Tasks, TaskTemplates, db
from webapp.todo.models import Reminders
from webapp.user.models import User

blueprint = Blueprint("APIv1", __name__, url_prefix="/todo/api/v1.0")


@dataclass
class TaskAPI:
    task_uri: str
    template_uri: str
    name: str
    description: str
    telegram_id: int | None = None
    time: str | None = None
    is_active: bool | None = None
    task_done: bool | None = None


@blueprint.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)


@blueprint.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({"error": "Bad Request"}), 400)


@blueprint.errorhandler(401)
def unauthorized(error):
    return make_response(jsonify({"error": "Unauthorized"}), 401)


@blueprint.errorhandler(403)
def forbidden(error):
    return make_response(jsonify({"error": "Forbidden"}), 403)


def get_user():
    telegram = request.args.get("telegram")
    if not telegram:
        abort(401)
    query = User.query.filter_by(telegram_user=telegram).first_or_404()
    return query


def get_query_list(user):
    return (
        db.session.query(Tasks, TaskTemplates, func.max(Reminders.time_reminder))
        .join(TaskTemplates, Tasks.id_task == TaskTemplates.id)
        .join(Reminders, TaskTemplates.id == Reminders.id_task_template, isouter=True)
        .filter(Tasks.id_list == user.active_list)
        .filter(TaskTemplates.owner == user.id)
        .group_by(Tasks)
    )


def get_query_task(task_id):
    return (
        db.session.query(Tasks, TaskTemplates, func.max(Reminders.time_reminder))
        .join(TaskTemplates, Tasks.id_task == TaskTemplates.id)
        .join(Reminders, TaskTemplates.id == Reminders.id_task_template, isouter=True)
        .filter(Tasks.id == task_id)
    )


def serialize_query(query) -> TaskAPI:
    return TaskAPI(
        task_uri=url_for("APIv1.get_task", task_id=query[0].id, _external=True),
        template_uri=url_for("APIv1.update_task_template", task_template_id=query[1].id, _external=True),
        name=query[1].name,
        description=query[1].description,
        time=query[2].strftime("%H:%M") if query[2] else "",
        is_active=query[1].is_active,
        task_done=query[0].task_done,
    )


@blueprint.route("/tasks/", methods=["GET"])
# @login_required_API
def get_tasks():
    user = get_user()

    query = get_query_list(user).all()

    tasks = []
    for task in query:
        tasks.append(serialize_query(task))
    return jsonify({"tasks": tasks})


@blueprint.route("/tasks/<int:task_id>", methods=["GET"])
# @login_required_API
def get_task(task_id):
    user = get_user()
    query = get_query_task(task_id).first_or_404()

    if query[1].owner != user.id:
        abort(403)

    task = serialize_query(query)
    return jsonify({"task": task})


@blueprint.route("/tasks/<int:task_id>", methods=["PUT"])
# @login_required_API
def update_task(task_id):
    user = get_user()
    query = get_query_task(task_id).first_or_404()

    if query[1].owner != user.id:
        abort(403)
    if not request.json:
        abort(400)
    if "task_done" in request.json and type(request.json["task_done"]) is not bool:
        abort(400)

    query[0].task_done = request.json.get("task_done", query[0].task_done)
    db.session.commit()

    query = get_query_task(task_id).first_or_404()
    task = serialize_query(query)

    return jsonify({"task": task})


@blueprint.route("/templates", methods=["GET"])
# @login_required_API
def get_task_templates():
    user = get_user()
    task_templates = TaskTemplates.query.filter_by(owner=user.id).all()
    return jsonify({"task_templates": [i.serialize for i in task_templates]})


@blueprint.route("/templates/<int:task_template_id>", methods=["PUT"])
# @login_required_API
def update_task_template(task_template_id):
    user = get_user()
    query = TaskTemplates.query.filter_by(id=task_template_id).first_or_404()

    if query.owner != user.id:
        abort(403)
    if not request.json:
        abort(400)
    if "is_active" in request.json and type(request.json["is_active"]) is not bool:
        abort(400)

    query.is_active = request.json.get("is_active", query.is_active)
    db.session.commit()

    query = TaskTemplates.query.filter_by(id=task_template_id).first_or_404()

    return jsonify({"task_templates": query.serialize})


@blueprint.route("/tasks/time/<time>", methods=["GET"])
def get_tasks_for_notification(time: str):
    # today: date = date.today()
    # reminder_time: str = datetime.now().strftime("%H:%M")
    query = (
        db.session.query(
            Tasks.id,
            Tasks.task_done,
            TaskTemplates.id,
            TaskTemplates.name,
            TaskTemplates.description,
            TaskTemplates.is_active,
            Reminders.time_reminder,
            User.telegram_id,
        )
        #  .join(ToDoLists, Tasks.id_list == ToDoLists.id)
        .join(TaskTemplates, Tasks.id_task == TaskTemplates.id)
        .join(Reminders, TaskTemplates.id == Reminders.id_task_template)
        .join(User, TaskTemplates.owner == User.id)
        .filter(User.active_list == Tasks.id_list)
        .filter(Reminders.time_reminder == time)
        .all()
    )

    tasks = []
    for task in query:
        print(task)
        print(url_for("APIv1.get_task", task_id=task[0], _external=True))
        tasks.append(
            TaskAPI(
                task_uri=url_for("APIv1.get_task", task_id=task[0], _external=True),
                task_done=task[1],
                template_uri=url_for("APIv1.update_task_template", task_template_id=task[2], _external=True),
                name=task[3],
                description=task[4],
                is_active=task[5],
                time=task[6].strftime("%H:%M") if task[6] else "",
                telegram_id=task[7],
            )
        )
    return jsonify({"tasks": tasks})
