import logging

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from webapp.db import db
from webapp.task_template.forms import TaskTemplateForm
from webapp.task_template.models import Reminder, TaskTemplate
from webapp.todo.models import Task

blueprint = Blueprint("templates", __name__, url_prefix="/templates")


@blueprint.route("/")
def list_templates():
    if not current_user.is_authenticated:
        return redirect(url_for("user.login"))
    task_templates = TaskTemplate.query.filter_by(owner=current_user.id).all()
    return render_template("task_template/list.html", task_templates=task_templates)


@blueprint.route("/add", methods=["GET", "POST"])
@login_required
def add_template():
    if not current_user.is_authenticated:
        return redirect(url_for("user.login"))
    form = TaskTemplateForm()
    return render_template("task_template/add.html", form=form)


@blueprint.route("/process-save-template", methods=["POST"])
def process_save_template():
    form = TaskTemplateForm()
    if form.validate_on_submit():
        new_task_template = TaskTemplate(
            name=form.name.data,
            description=form.description.data,
            owner=current_user.id,
        )
        db.session.add(new_task_template)
        db.session.commit()
        logging.info(f"{new_task_template} created")

        new_task = Task(date_id=current_user.active_date, task_template_id=new_task_template.id)
        db.session.add(new_task)
        if form.to_time.data:
            new_time = Reminder(
                task_template_id=new_task_template.id, reminder_time=form.to_time.data
            )
            db.session.add(new_time)
        db.session.commit()
        logging.info(f"{new_task} created")
        logging.info(f"{new_time} created")
        flash("Задача добавлена!")
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash('Ошибка в поле "{}": - {}'.format(getattr(form, field).label.text, error))
    return redirect(url_for("templates.add_template"))
