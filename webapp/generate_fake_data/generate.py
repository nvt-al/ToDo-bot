import csv
import random

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
    return random.choice(template)  # nosec


def generation_user_templates():
    tasks_templates = []

    users = User.query.all()
    for user in users:
        templates = set()
        number_user_templates: int = random.randint(3, 7)  # nosec
        for _ in range(number_user_templates):
            templates.add(get_task_template())
        for template in templates:
            description = "" if random.randint(0, 1) else f"Описание задачи {template}"  # nosec
            is_active = random.randint(0, 1)  # nosec
            tasks_templates.append([template, user.id, description, is_active])
    return tasks_templates
