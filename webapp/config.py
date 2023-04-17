import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "..", "todo.db")
SECRET_KEY = os.getenv("SECRET_KEY", "")
SQLALCHEMY_TRACK_MODIFICATIONS = False
