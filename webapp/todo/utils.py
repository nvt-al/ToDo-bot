import logging
from datetime import date

from webapp.db import db
from webapp.task_template.models import TaskTemplate
from webapp.todo.models import Date, Task
from webapp.user.models import User


def get_today_id() -> int:
    today: date = date.today()
    today_id = db.session.query(Date.id).filter(Date.name == today.strftime("%Y-%m-%d")).first()
    if today_id:
        return today_id.id
    else:
        return add_date(today).id


def add_date(day: date) -> Date:
    today = Date.query.filter_by(name=day.strftime("%Y-%m-%d")).first()
    if not today:
        new_date = Date(name=day)
        db.session.add(new_date)
        db.session.commit()
        logging.info(f"{new_date} created")
        return new_date
    else:
        logging.info(f"{today} already exists")
        return today


def add_tasks_in_todolist(todolist_id: int) -> None:
    logging.info("run add_task_in_todolist")
    tasks_list = db.session.query(Task.task_template_id).filter(Task.id_list == todolist_id)
    task_templates = (
        db.session.query(TaskTemplate.id)
        .filter(TaskTemplate.is_active, TaskTemplate.id.notin_(tasks_list))
        .all()
    )
    new_task_templates: list[Task] = []
    for template in task_templates:
        new_task_templates.append(Task(id_list=todolist_id, id_task=template.id))
    db.session.bulk_save_objects(new_task_templates)
    users = User.query.filter(User.active_date < todolist_id).all()
    for user in users:
        user.active_list = todolist_id
    db.session.commit()
