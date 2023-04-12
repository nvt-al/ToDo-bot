from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, TimeField
from wtforms.validators import DataRequired, Length, Optional, ValidationError


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
    # list_name = StringField(
    #     "Введите текст: ",
    #     validators=[
    #         DataRequired(),
    #         Length(min=1, max=100, message="Текст должен быть от 1 до 100 символов"),
    #     ],
    # )

    to_time = TimeField("Введите время", format="%H:%M", validators=[Optional()])
    to_date = DateField("Введите дату", format="%Y-%m-%d", validators=[DataRequired()])
