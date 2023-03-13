from flask_sqlalchemy import SQLAlchemy, model

db = SQLAlchemy()
Base: model = db.Model


class TaskTemplates(Base):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    owner = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "<Задача {} {}>".format(self.id, self.name)


class Statuses(Base):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def __repr__(self):
        return "<Статус {} {}>".format(self.id, self.name)


class Lists(Base):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def __repr__(self):
        return "<Имя списка {}>".format(self.name)


class ToDoList(Base):
    id = db.Column(db.Integer, primary_key=True)
    id_task = db.Column(db.Integer, nullable=False)
    id_list = db.Column(db.Integer, nullable=False)
    task_done = db.Column(db.Boolean)

    def __repr__(self):
        return "<Имя списка {}>".format(self.name)
