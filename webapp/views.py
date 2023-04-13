from flask import Blueprint, render_template, url_for, redirect, flash, abort, request
from flask_login import login_required, current_user
from datetime import datetime
from webapp.forms import TaskForm, CreateList
from webapp.models import TaskTemplates, Tasks, ToDoLists, db


tasks_bp = Blueprint("tasks", __name__)


def create_task_list(form):
    selected_tasks = request.form.getlist("list_task")
    selected_tasks = [int(task_id) for task_id in selected_tasks]
    selected_tasks = TaskTemplates.query.filter(
        TaskTemplates.id.in_(selected_tasks)
    ).all()
    name = ToDoLists(name=form.list_name.data)
    db.session.add(name)
    for task in selected_tasks:
        new_task = Tasks(task_template=task, todo_list=name)
        db.session.add(new_task)
    db.session.commit()
    flash("Список создан!")


@tasks_bp.route("/", methods=["GET", "POST"])
# @login_required  при добавлении ошибка c login
def index():
    form = CreateList()
    tasks = TaskTemplates.query.all()
    # tasks = TaskTemplates.query.filter_by(owner=current_user.id).all()   при добавлении не видит user.id
    if form.validate_on_submit():
        create_task_list(form)
        return redirect(url_for("tasks.index"))
    return render_template("index.html", tasks=tasks, form=form)


@tasks_bp.route("/lists", methods=["GET", "POST"])
@login_required
def lists():
    form = CreateList()
    task_templates = TaskTemplates.query.filter_by(owner=current_user.id).all()
    todo_lists = ToDoLists.query.all()
    # todo_lists = ToDoLists.query.filter_by(owner=current_user.id).all()            вместо owner что вставить?
    if form.validate_on_submit():
        create_task_list(form)
        return redirect(url_for("tasks.lists"))
    return render_template(
        "lists.html", task_templates=task_templates, todo_lists=todo_lists, form=form
    )


@tasks_bp.route("/add_task", methods=["GET", "POST"])
@login_required
def add_task():
    form = TaskForm()
    if form.validate_on_submit():
        new_task = TaskTemplates(
            name=form.name_task.data.capitalize(),
            description=form.description.data.capitalize(),
            owner=current_user.id,
            is_active=False
        )
        db.session.add(new_task)
        db.session.commit()
        flash("Задача добавлена!")
        return redirect(url_for("tasks.index"))
    return render_template("add_task.html", form=form)


@tasks_bp.route("/update/<int:task_id>", methods=["GET", "POST"])
@login_required
def update(task_id):
    task = TaskTemplates.query.filter_by(id=task_id).first()
    if task.owner != current_user.id:
        abort(403)
    task.is_active = not task.is_active
    db.session.commit()
    return redirect(url_for("tasks.index"))


@tasks_bp.route("/delete/<int:task_id>", methods=["GET", "POST"])
@login_required
def delete_task(task_id):
    task = TaskTemplates.query.filter_by(id=task_id).first_or_404()
    if task.owner != current_user.id:
        abort(403)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("tasks.index"))
