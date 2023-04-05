from datetime import date

from webapp import create_app
from webapp.models import Tasks, TaskTemplates, ToDoLists, db


def add_todolist(day: date) -> ToDoLists:
    today_list = ToDoLists.query.filter_by(name=day).first()
    if not today_list:
        new_list = ToDoLists(name=today)
        db.session.add(new_list)
        db.session.commit()
        print(f"{new_list} создан")
        return new_list
    else:
        print(f"{today_list} уже существует")
        return today_list


def add_tasks_in_todolist(todolist: ToDoLists) -> None:
    tasks_list = db.session.query(Tasks.id_task).filter(Tasks.id_list == todolist.id)
    task_templates = (
        db.session.query(TaskTemplates.id).filter(TaskTemplates.is_active, TaskTemplates.id.notin_(tasks_list)).all()
    )
    print(task_templates)
    # for template in task_templates:


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        today: date = date.today()
        # today = date(2023, 3, 22)
        today_list = add_todolist(today)
        add_tasks_in_todolist(today_list)
