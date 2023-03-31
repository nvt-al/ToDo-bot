from flask import Blueprint, render_template, url_for, redirect, flash, request
from webapp.forms import TaskForm
from webapp.models import TaskTemplates, db

page = Blueprint("tasks", __name__, url_prefix="/add_task")

@page.route("/add_task", methods=["GET", "POST"])
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


# update task
# @bp.routes.route("/update_task/<int:task_id>", methods=["GET", "POST"])
# def update(task_id):
# task = Tasks.query.filter_by(id=task_id).first()
# if request.method == "POST":
#     task.is_active = not task.is_active
#     db.session.commit()
#     return redirect(url_for("index"))
# return render_template("update_task.html", task=task)

# # delete task
# @bp.route("/delete_task/<int:task_id>", methods=["POST"])
# def delete_task(task_id):
# task = Tasks.query.filter_by(id=task_id).first()
# db.session.delete(task)
# db.session.commit()
# flash("Задача удалена!")
# return redirect(url_for("index"))

# @bp.route("/report")
# def look_report():
# tasks = Tasks.query.all()
# return render_template("report.html", tasks=tasks)
