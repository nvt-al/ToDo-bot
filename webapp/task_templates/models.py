from datetime import time

from webapp.db import Base, db


class TaskTemplates(Base):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    owner = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    def __repr__(self):
        return "<Задача {} {}>".format(self.id, self.name)

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {"id": self.id, "name": self.name, "description": self.description, "is_active": self.is_active}


class Reminders(Base):
    id = db.Column(db.Integer, primary_key=True)
    id_task_template = db.Column(db.Integer, db.ForeignKey("task_templates.id"), nullable=False)
    time_reminder = db.Column(db.Time, default=time(8, 0), nullable=False)

    def __repr__(self):
        return "<Время напоминание {} для задачи {}>".format(self.time_reminder, self.id_task_template)
