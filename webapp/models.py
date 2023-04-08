from flask_sqlalchemy import SQLAlchemy, model
from sqlalchemy import MetaData
from sqlalchemy.orm import relationship

metadata = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)
db = SQLAlchemy(metadata=metadata)
Base: model = db.Model


class TaskTemplates(Base):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    owner = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    def __repr__(self):
        return "<Задача {} {}>".format(self.id, self.name)


class ToDoLists(Base):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def __repr__(self):
        return "<Имя ToDo списка {}>".format(self.name)


class Tasks(Base):
    id = db.Column(db.Integer, primary_key=True)
    id_task = db.Column(db.Integer, db.ForeignKey("task_templates.id"), nullable=False)
    id_list = db.Column(db.Integer, db.ForeignKey("to_do_lists.id"), nullable=False)
    task_done = db.Column(db.Boolean, default=False)

    task_template = relationship("TaskTemplates", backref="tasks")
    todo_list = relationship("ToDoLists", backref="tasks")

    def __repr__(self):
        return "<Задача {} из списка {}>".format(self.id_task, self.id_list)
