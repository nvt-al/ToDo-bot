from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, DateTimeField, TimeField, SelectField
from wtforms.validators import DataRequired


class TaskForm(FlaskForm):
    new_task = StringField('Введите текст: ', validators=[DataRequired()])
    description_task = StringField('Введите описание: ', validators=[DataRequired()])
    to_time = TimeField('Введите время', format='%H:%M')
    to_date= DateField('Введите дату', format='%H:%M:%S')
    status = SelectField('Статус', choices=[('Выполнено', 'Выполнено'), ('Ожидается', 'Ожидается ')])
    submit = SubmitField('Создать новое напоминание')

    # submit_yes = SubmitField('Выполнено')
    # submit_del = SubmitField('Отменить')


    