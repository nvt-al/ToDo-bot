from datetime import date, datetime

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
    with flask_app.app_context():
        today: date = date.today()
        # today = date(2023, 3, 22)
        today_list = tasks.add_todolist(today)
        tasks.add_tasks_in_todolist(today_list.id)


@celery_app.task
def send_notification() -> None:
    with flask_app.app_context():
        today: date = date.today()
        reminder_time: str = datetime.now().strftime("%H:%M")
        tasks.notification(today, reminder_time)


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs) -> None:
    sender.add_periodic_task(crontab(hour="0"), create_new_day.s())
    sender.add_periodic_task(crontab(minute="*/1"), send_notification.s())


if __name__ == "__main__":
    create_new_day()
