from datetime import time

from webapp.db import Base, db


class TaskTemplate(Base):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    owner = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    def __repr__(self):
        return "<TaskTemplate: {} {}>".format(self.id, self.name)

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "is_active": self.is_active,
        }


class Reminder(Base):
    id = db.Column(db.Integer, primary_key=True)
    task_template_id = db.Column(
        db.Integer, db.ForeignKey("task_template.id", ondelete="CASCADE"), nullable=False
    )
    reminder_time = db.Column(db.Time, default=time(8, 0), nullable=False)

    def __repr__(self):
        return "<Reminder: time {}, TaskTemplate {}>".format(
            self.reminder_time, self.task_template_id
        )
