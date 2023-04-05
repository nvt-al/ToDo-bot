from flask import Blueprint, render_template, url_for, redirect, flash, request
from flask_login import current_user, login_user
from webapp.user.models import User
from webapp.forms import TaskForm
from webapp.models import TaskTemplates, db


page = Blueprint("tasks", __name__)


@page.route("/")
def index():
    form = TaskForm()
    tasks = TaskTemplates.query.all()
    return render_template("index.html", tasks=tasks, form=form)


@page.route("/add_task", methods=["GET", "POST"])
# @login_required
def add_task():
    form = TaskForm()
    if form.validate_on_submit():
        name = request.form.get("name_task")
        description = request.form.get("description")
        new_task = TaskTemplates(
            name=name, description=description, owner=1, is_active=False
        )
        db.session.add(new_task)
        db.session.commit()
        flash("Задача добавлена!")
        return redirect(url_for("tasks.index"))
    return render_template("add_task.html", form=form)


@page.route("/update/<int:task_id>", methods=["GET", "POST"])
# @login_required
def update(task_id):
    task = TaskTemplates.query.filter_by(id=task_id).first()
    # if task.owner != current_user.id:
    #     abort(403)
    task.is_active = not task.is_active
    db.session.commit()
    return redirect(url_for("tasks.index"))


@page.route("/delete/<int:task_id>", methods=["POST", "GET"])
# @login_required
def delete_task(task_id):
    task = TaskTemplates.query.filter_by(id=task_id).first_or_404()
    # if task.owner != current_user.id:
    #     abort(403)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("tasks.index"))


@page.route("/lists")
def show_lists():
    tasks = TaskTemplates.query.all()

    return render_template("lists.html", tasks=tasks)
