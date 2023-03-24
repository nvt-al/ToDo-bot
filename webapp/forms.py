from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    DateField,
    TimeField,
    SelectField,
)
from wtforms.validators import DataRequired


class TaskForm(FlaskForm):
    name_task = StringField("Введите текст: ", validators=[DataRequired()])
    description = StringField("Введите описание: ", validators=[DataRequired()])
    to_time = TimeField("Введите время", format="%H:%M")
    to_date = DateField("Введите дату", format="%H:%M:%S")
    status = SelectField(
        "Статус", choices=[("Выполнено", "Выполнено"), ("Ожидается", "Ожидается ")]
    )
    submit = SubmitField("Создать новое напоминание")
    delete_task = SubmitField("Удалить")
    edit_task = SubmitField("Редактировать")
