import csv
from datetime import datetime, timedelta
from random import choice, randint

from webapp.models import Tasks, TaskTemplates, ToDoLists, db
from webapp.user.models import User


def get_task_template():
    template = [
        "Утреняя зарядка",
        "Тренажерный зал",
        "Принять лекарства",
        "Изучение слов ин.яз",
        "Аудирование ин.яз",
        "Говорение ин.яз",
        "Изучение Python",
        "Изучение JS",
        "Изучение SQL",
        "Чтение",
    ]
    return choice(template)  # nosec


def generate_user_templates():
    tasks_templates = []

    users = User.query.all()
    for user in users:
        templates = set()
        number_user_templates: int = randint(3, 7)  # nosec
        for _ in range(number_user_templates):
            templates.add(get_task_template())
        for template in templates:
            description = "" if randint(0, 1) else f"Описание задачи {template}"  # nosec
            is_active = randint(0, 1)  # nosec
            tasks_templates.append(
                {"name": template, "owner": user.id, "description": description, "is_active": bool(is_active)}
            )
    return tasks_templates


def generate_todo_lists():
    number_deys = 10
    todo_lists = []
    for i in reversed(range(number_deys)):
        todo_lists.append({"name": datetime.strftime(datetime.today() - timedelta(days=i), "%Y-%m-%d")})
    return todo_lists


def generate_tasks():
    todo_lists = ToDoLists.query.all()
    templates = TaskTemplates.query.all()
    tasks = []
    for list in todo_lists:
        for template in templates:
            if randint(0, 1):  # nosec
                tasks.append({"id_task": template.id, "id_list": list.id, "task_done": randint(0, 1)})  # nosec
    return tasks


def generate_fake_data():
    user_templates = generate_user_templates()
    todo_lists = generate_todo_lists()
    db.session.bulk_insert_mappings(TaskTemplates, user_templates)
    db.session.bulk_insert_mappings(ToDoLists, todo_lists)
    db.session.commit()
    tasks = generate_tasks()
    db.session.bulk_insert_mappings(Tasks, tasks)
    db.session.commit()
