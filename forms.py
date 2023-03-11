from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, DateTimeField, TimeField
from wtforms.validators import DataRequired


class TaskForm(FlaskForm):
    new_task = StringField('Введите текст: ', validators=[DataRequired()])
    submit = SubmitField('Создать новое напоминание')
    to_time = TimeField('Введите время', format='%H:%M')
    to_date= DateField('Введите дату', format='%H:%M:%S')
    submit_yes = SubmitField('Выполнено')
    submit_del = SubmitField('Отменить')


    