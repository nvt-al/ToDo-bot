from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class TaskForm(FlaskForm):
    # new_task = StringField('Введите текст', validators=[DataRequired()])
    submit = SubmitField('Создать новое напоминание',render_kw={"class":"btn btn-primary"})
    # date = StringField('Дата', validators=[DataRequired()])
    # time = StringField('Время', validators=[DataRequired()])
