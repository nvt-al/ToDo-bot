from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, TimeField, SelectMultipleField
from wtforms.validators import DataRequired, Length, Optional, ValidationError


class CreateList(FlaskForm):
    list_name = StringField(
        "Название списка",
        validators=[DataRequired()],
        render_kw={"class": "form-control"},
    )
    # list_task = SelectMultipleField(
    #     "Задачи",
    #     choices=[("task1", "Задача 1"), ("task2", "Задача 2"), ("task3", "Задача 3")],
    #     validators=[DataRequired()],
    #     render_kw={"class": "form-control"},
    # )
    submit = SubmitField("Создать!", render_kw={"class": "btn btn-primary"})


class TaskForm(FlaskForm):
    name_task = StringField(
        "Введите текст: ",
        validators=[
            DataRequired(),
            Length(min=1, max=100, message="Текст должен быть от 1 до 100 символов"),
        ],
    )
    description = StringField(
        "Введите описание: ",
        validators=[
            DataRequired(),
            Length(min=1, max=500, message="Описание должно быть от 1 до 500 символов"),
        ],
    )

    to_time = TimeField("Введите время", format="%H:%M", validators=[Optional()])
    to_date = DateField("Введите дату", format="%Y-%m-%d", validators=[DataRequired()])
