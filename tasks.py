from celery import Celery

from webapp import create_app

flask_app = create_app()
celery_app = Celery("tasks", broker="redis://127.0.0.1:6379/0")


@celery_app.task
def add(x, y):
    print(x + y)
