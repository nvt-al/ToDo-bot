from datetime import date

from webapp import create_app
from webapp.models import ToDoLists, db

today: date = date.today()


app = create_app()
with app.app_context():
    today_list = ToDoLists.query.filter_by(name=today).first()
    if not today_list:
        new_list = ToDoLists(name=today)
        db.session.add(new_list)
        db.session.commit()
        print(f"{new_list} создан")
    else:
        print(f"{today_list} уже существует")
