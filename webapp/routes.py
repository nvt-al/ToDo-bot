from flask import Flask, render_template, url_for, redirect, flash, request
from models import TaskTemplates, ToDoLists, Tasks, db
from forms import TaskForm


app = Flask(__name__)


@app.route("/")
def index():
    all_tasks = Tasks.query.all()
    return render_template(url_for("index"), all_tasks=all_tasks)


# add new task
@app.route("/add_task", methods=["GET", "POST"])
def add_task():
    form = TaskForm()
    if request.method == "POST" and form.validate_on_submit():
        name = form.name.data
        new_task = Tasks(name=name, is_active=False)
        db.session.add(new_task)
        db.session.commit()
        flash("Задача успешно добавлена!")
        return redirect(url_for("index"))
    return render_template("add_task.html", form=form)


# update task
@app.route("/update_task/<int:task_id>", methods=["GET", "POST"])
def update(task_id):
    task = Tasks.query.filter_by(id=task_id).first()
    if request.method == "POST":
        task.is_active = not task.is_active
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("update_task.html", task=task)


# delete task
@app.route("/delete_task/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    task = Tasks.query.filter_by(id=task_id).first()
    db.session.delete(task)
    db.session.commit()
    flash("Задача удалена!")
    return redirect(url_for("index"))


@app.route("/report")
def look_report():
    tasks = Tasks.query.all()
    return render_template("report.html", tasks=tasks)


if __name__ == "__main__":
    app.run(debug=True)
