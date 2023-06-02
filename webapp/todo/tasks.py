import logging
from datetime import date

from webapp.models import Tasks, TaskTemplates, ToDoLists, db
from webapp.user.models import User


def add_todolist(day: date) -> ToDoLists:
    today = ToDoLists.query.filter_by(name=day).first()
    if not today:
        new_list = ToDoLists(name=day)
        db.session.add(new_list)
        db.session.commit()
        logging.info(f"{new_list.name} created")
        return new_list
    else:
        logging.info(f"{today.name} already exists")
        return today


def add_tasks_in_todolist(todolist_id: int) -> None:
    logging.info("run add_task_in_todolist")
    tasks_list = db.session.query(Tasks.id_task).filter(Tasks.id_list == todolist_id)
    task_templates = (
        db.session.query(TaskTemplates.id).filter(TaskTemplates.is_active, TaskTemplates.id.notin_(tasks_list)).all()
    )
    new_task_templates: list[Tasks] = []
    for template in task_templates:
        new_task_templates.append(Tasks(id_list=todolist_id, id_task=template.id))
    db.session.bulk_save_objects(new_task_templates)
    users = User.query.filter(User.active_list < todolist_id).all()
    for user in users:
        user.active_list = todolist_id
    db.session.commit()
