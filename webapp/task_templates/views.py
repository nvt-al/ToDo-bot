import logging

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from webapp.db import db
from webapp.task_templates.forms import TaskTemplateForm
from webapp.task_templates.models import Reminders, TaskTemplates
from webapp.todo.models import Tasks

blueprint = Blueprint("templates", __name__, url_prefix="/templates")


@blueprint.route("/")
def list_templates():
    if not current_user.is_authenticated:
        return redirect(url_for("user.login"))
    # form = CreateList()
    # if login_required:
    task_templates = TaskTemplates.query.filter_by(owner=current_user.id).all()
    return render_template("task_templates/list.html", task_templates=task_templates)


@blueprint.route("/add", methods=["GET", "POST"])
@login_required
def add_template():
    if not current_user.is_authenticated:
        return redirect(url_for("user.login"))
    form = TaskTemplateForm()
    return render_template("task_templates/add.html", form=form)


@blueprint.route("/process-save-template", methods=["POST"])
def process_save_template():
    form = TaskTemplateForm()
    if form.validate_on_submit():
        new_task_template = TaskTemplates(
            name=form.name.data,
            description=form.description.data,
            owner=current_user.id,
        )
        db.session.add(new_task_template)
        db.session.commit()

        new_task = Tasks(id_list=current_user.active_list, id_task=new_task_template.id)
        db.session.add(new_task)
        if form.to_time.data:
            new_time = Reminders(id_task_template=new_task_template.id, time_reminder=form.to_time.data)
            db.session.add(new_time)
        db.session.commit()
        flash("Задача добавлена!")
    flash("")
    return redirect(url_for("templates.add_template"))
