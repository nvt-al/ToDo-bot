from webapp.db import Base, db


class ToDoLists(Base):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)

    def __repr__(self):
        return "<Имя ToDo списка {}>".format(self.name)


class Tasks(Base):
    id = db.Column(db.Integer, primary_key=True)
    id_task = db.Column(db.Integer, db.ForeignKey("task_templates.id"), nullable=False)
    id_list = db.Column(db.Integer, db.ForeignKey("to_do_lists.id"), nullable=False)
    task_done = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return "<Задача №{} из списка {}>".format(self.id_task, self.id_list)


# class Repeatability(Base):
#     id = db.Column(db.Integer, primary_key=True)
#     id_task_template = db.Column(db.Integer, db.ForeignKey("task_templates.id"), nullable=False)
#     day_start = db.Column(db.Date, default=date.today())
#     day_end = db.Column(db.Date, default=None)
#     id_unit_time = db.Column(db.Integer, db.ForeignKey("units_time.id"), nullable=False)
#     interval = db.Column(db.Integer, nullable=False, default=1)

#     def __repr__(self):
#         return "<Повтор № {} для задачи {}>".format(self.id, self.id_task_template)


# class UnitsTime(Base):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, nullable=False)

#     def __repr__(self):
#         return "<Еденица измерения №{} {}>".format(self.id, self.name)
