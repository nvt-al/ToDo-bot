from datetime import date

from webapp.models import Base, db


class Repeatability(Base):
    id = db.Column(db.Integer, primary_key=True)
    id_task_template = db.Column(db.Integer, db.ForeignKey("task_templates.id"), nullable=False)
    day_start = db.Column(db.Date, default=date.today())
    day_end = db.Column(db.Date, default=date.today())
    id_unit_time = db.Column(db.Integer, db.ForeignKey("task_templates.id"), nullable=False)
    interval = db.Column(db.Integer, nullable=False, default=1)

    def __repr__(self):
        return "<Повтор № {} для задачи {}>".format(self.id, self.id_task_template)
