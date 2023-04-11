import logging
from datetime import date

from celery import Celery
from celery.schedules import crontab
from pytz import timezone

from webapp import create_app
from webapp.todo import tasks

flask_app = create_app()
celery_app = Celery("tasks", broker="redis://127.0.0.1:6379/0")
celery_app.timezone = timezone("Europe/Moscow")


@celery_app.task
def create_new_day() -> None:
    logging.info("task new day")
    with flask_app.app_context():
        today: date = date.today()
        today_list = tasks.add_todolist(today)
        tasks.add_tasks_in_todolist(today_list.id)


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs) -> None:
    logging.info("periodic tasks")
    sender.add_periodic_task(crontab(minute=0, hour="*/1"), create_new_day.s())


if __name__ == "__main__":
    create_new_day()
