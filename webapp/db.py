from flask_sqlalchemy import SQLAlchemy, model

db = SQLAlchemy()
Base: model = db.Model
