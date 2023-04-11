from datetime import date, time

from webapp.models import Base, db


class Repeatability(Base):
    id = db.Column(db.Integer, primary_key=True)
    id_task_template = db.Column(db.Integer, db.ForeignKey("task_templates.id"), nullable=False)
    day_start = db.Column(db.Date, default=date.today())
    day_end = db.Column(db.Date, default=None)
    id_unit_time = db.Column(db.Integer, db.ForeignKey("units_time.id"), nullable=False)
    interval = db.Column(db.Integer, nullable=False, default=1)

    def __repr__(self):
        return "<Повтор № {} для задачи {}>".format(self.id, self.id_task_template)


class UnitsTime(Base):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def __repr__(self):
        return "<Еденица измерения №{} {}>".format(self.id, self.name)


class Reminders(Base):
    id = db.Column(db.Integer, primary_key=True)
    id_task_template = db.Column(db.Integer, db.ForeignKey("task_templates.id"), nullable=False)
    time_reminder = db.Column(db.Time, default=time(8, 0), nullable=False)

    def __repr__(self):
        return "<Время напоминание {} для задачи {}>".format(self.time_reminder, self.id_task_template)
