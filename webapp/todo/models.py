from webapp.db import Base, db


class Date(Base):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)

    def __repr__(self):
        return "<Date: {}>".format(self.name)


class Task(Base):
    id = db.Column(db.Integer, primary_key=True)
    task_template_id = db.Column(
        db.Integer, db.ForeignKey("task_template.id", ondelete="CASCADE"), nullable=False
    )
    date_id = db.Column(db.Integer, db.ForeignKey("date.id", ondelete="CASCADE"), nullable=False)
    is_done = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return "<Task: {}>".format(self.id)
