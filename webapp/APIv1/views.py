from flask import Blueprint, abort, jsonify, make_response, request, url_for

# from webapp.APIv1.decorators import login_required_API
from webapp.models import Tasks, TaskTemplates, db
from webapp.user.models import User

blueprint = Blueprint("APIv1", __name__, url_prefix="/todo/api/v1.0/tasks")


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
    query = User.query.filter_by(telegram_user=telegram).first_or_404()
    return query


@blueprint.route(
    "/",
    methods=["GET"],
)
# @login_required_API
def get_tasks():
    user = get_user()

    query = (
        db.session.query(Tasks, TaskTemplates)
        .join(TaskTemplates, Tasks.id_task == TaskTemplates.id)
        .filter(Tasks.id_list == user.active_list)
        .filter(TaskTemplates.owner == user.id)
        .all()
    )

    tasks = []
    for task in query:
        tasks.append(
            {
                "uri": url_for("APIv1.get_task", task_id=task[0].id, _external=True),
                "task_templates_id": task[1].id,
                "name": task[1].name,
                "description": task[1].description,
                "task_done": task[0].task_done,
            }
        )
    return jsonify({"tasks": tasks})


@blueprint.route("/<int:task_id>", methods=["GET"])
# @login_required_API
def get_task(task_id):
    user = get_user()
    query = (
        db.session.query(Tasks, TaskTemplates)
        .join(TaskTemplates, Tasks.id_task == TaskTemplates.id)
        .filter(Tasks.id == task_id)
        .first_or_404()
    )

    if query[1].owner != user.id:
        abort(403)

    task = {
        "task_id": query[0].id,
        "task_template_id": query[1].id,
        "name": query[1].name,
        "description": query[1].description,
        "is_active": query[1].is_active,
        "task_done": query[0].task_done,
    }
    return jsonify({"task": task})


@blueprint.route("/<int:task_id>", methods=["PUT"])
# @login_required_API
def update_task(task_id):
    user = get_user()
    query = (
        db.session.query(Tasks, TaskTemplates)
        .join(TaskTemplates, Tasks.id_task == TaskTemplates.id)
        .filter(Tasks.id == task_id)
        .first_or_404()
    )

    if query[1].owner != user.id:
        abort(403)
    if not request.json:
        abort(400)
    if "task_done" in request.json and type(request.json["task_done"]) is not bool:
        abort(400)

    query[0].task_done = request.json.get("task_done", query[0].task_done)
    db.session.commit()

    query = Tasks.query.filter_by(id=task_id).first()
    task = {"id": query.id, "task_done": query.task_done}

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