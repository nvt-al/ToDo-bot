from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class TaskForm(FlaskForm):
    new_task = StringField('Введите текст', validators=[DataRequired()])
    submit = SubmitField('Добавить')
   