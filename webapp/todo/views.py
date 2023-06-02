from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from webapp.db import db
from webapp.task_template.models import TaskTemplate
from webapp.todo.models import Date, Task

blueprint = Blueprint("tasks", __name__)


@blueprint.route("/")
def index():
    return render_template("index.html")


@blueprint.route("/update/<int:task_id>", methods=["GET", "POST"])
@login_required
def update(task_id):
    task = TaskTemplate.query.filter_by(id=task_id).first()
    if task.owner != current_user.id:
        abort(403)
    task.is_active = not task.is_active
    db.session.commit()
    return redirect(url_for("tasks.index"))


@blueprint.route("/delete/<int:task_id>", methods=["GET", "POST"])
@login_required
def delete_task(task_id):
    task = TaskTemplate.query.filter_by(id=task_id).first_or_404()
    if task.owner != current_user.id:
        abort(403)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("tasks.index"))


@blueprint.route("/report", methods=["GET", "POST"])
@login_required
def report(task_id):
    return render_template("report.html")
