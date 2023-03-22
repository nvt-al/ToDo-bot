from flask_wtf import FlaskForm
from wtforms import SubmitField


class GenerateDataForm(FlaskForm):
    submit = SubmitField("Генерировать данные", render_kw={"class": "btn btn-primary"})
