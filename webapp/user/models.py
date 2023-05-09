from datetime import time

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from webapp.db import Base, db


class User(Base, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))
    email = db.Column(db.String(50))
    telegram_user = db.Column(db.String(50))
    telegram_id = db.Column(db.Integer)
    active_list = db.Column(db.Integer, db.ForeignKey("to_do_lists.id"))
    default_reminder_time = db.Column(db.Time, default=time(12, 0))
    time_start_new_day = db.Column(db.Time, nullable=False, default=time(0, 0))
    week_report = db.Column(db.Boolean, default=False)
    month_report = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return "<User {}>".format(self.username)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
