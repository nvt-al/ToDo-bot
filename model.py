from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Tasks(db.Model):  # Name "db.Model" is not defined  [name-defined] mypy(error)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    owner = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Задача {} {}>'.format(self.id, self.name)

# class lists(db.Model: Model):
#     id = db.Column(db.Integer, primary_key=True)
