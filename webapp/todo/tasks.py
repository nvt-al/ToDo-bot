import logging
from datetime import date

from webapp.models import Tasks, TaskTemplates, ToDoLists, db
from webapp.user.models import User


def add_todolist(day: date) -> ToDoLists:
    today_list = ToDoLists.query.filter_by(name=day).first()
    if not today_list:
        new_list = ToDoLists(name=day)
        db.session.add(new_list)
        db.session.commit()
        logging.info(f"{new_list} created")
        return new_list
    else:
        logging.info(f"{today_list} already exists")
        return today_list


def add_tasks_in_todolist(todolist_id: int) -> None:
    logging.info("run add_task_in_todolist")
    tasks_list = db.session.query(Tasks.id_task).filter(Tasks.id_list == todolist_id)
    task_templates = (
        db.session.query(TaskTemplates.id).filter(TaskTemplates.is_active, TaskTemplates.id.notin_(tasks_list)).all()
    )
    new_task_templates: list[Tasks] = []
    for template in task_templates:
        new_task_templates.append(Tasks(id_list=todolist_id, id_task=template.id))
    logging.info(new_task_templates)
    db.session.bulk_save_objects(new_task_templates)
    users = User.query.all()
    for user in users:
        user.active_list = todolist_id
        logging.info(user, user.active_list)
    db.session.commit()
