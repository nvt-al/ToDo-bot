from flask_sqlalchemy import SQLAlchemy, model

db = SQLAlchemy()
Base: model = db.Model


class TaskTemplates(Base):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    owner = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    id_status = db.Column(db.Integer, db.ForeignKey("statuses.id"), nullable=False)

    def __repr__(self):
        return "<Задача {} {}>".format(self.id, self.name)


class Statuses(Base):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def __repr__(self):
        return "<Статус {} {}>".format(self.id, self.name)


class ToDoLists(Base):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def __repr__(self):
        return "<Имя ToDo списка {}>".format(self.name)


class Tasks(Base):
    id = db.Column(db.Integer, primary_key=True)
    id_task = db.Column(db.Integer, db.ForeignKey("task_templates.id"), nullable=False)
    id_list = db.Column(db.Integer, db.ForeignKey("to_do_lists.id"), nullable=False)
    task_done = db.Column(db.Boolean)

    def __repr__(self):
        return "<Задача {} из спска {}>".format(self.id_task, self.id_list)
