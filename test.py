from webapp import create_app
from webapp.todo.utils import get_today_id

flask_app = create_app()


if __name__ == "__main__":
    with flask_app.app_context():
        print(get_today_id())
