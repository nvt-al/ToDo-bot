from datetime import date

from celery import Celery
from celery.schedules import crontab

from webapp import create_app
from webapp.todo import add_tasks

flask_app = create_app()
celery_app = Celery("tasks", broker="redis://127.0.0.1:6379/0")


@celery_app.task
def create_new_day() -> None:
    with flask_app.app_context():
        today: date = date.today()
        # today = date(2023, 3, 22)
        today_list = add_tasks.add_todolist(today)
        add_tasks.add_tasks_in_todolist(today_list.id)


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs) -> None:
    sender.add_periodic_task(crontab(hour="0"), create_new_day.s())
